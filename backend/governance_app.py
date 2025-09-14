#!/usr/bin/env python3
"""
AI Governance Platform - Flask Web Application
Comprehensive enterprise AI governance platform with REST API
"""

import os
import sys
import logging
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents import (
    create_governance_pipeline,
    WorkflowType,
    example_comprehensive_assessment,
    example_rapid_screening
)
from agents.risk_agent import RiskAssessmentAgent
from agents.bias_agent import BiasDetectionAgent
from database.sqlite_manager import SQLiteManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Global variables for governance components
governance_db = None
knowledge_store = None
orchestrator = None

def initialize_governance_platform():
    """Initialize the governance platform components"""
    global governance_db, knowledge_store, orchestrator

    try:
        # Initialize database
        governance_db = SQLiteManager("database/governance_data.db")
        knowledge_store = None  # Mock for now

        # Create orchestrator
        orchestrator = create_governance_pipeline(knowledge_store, governance_db, "standard")

        logger.info("AI Governance Platform initialized successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to initialize governance platform: {str(e)}")
        return False

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Governance Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: #f5f7fa; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; text-align: center; border-radius: 10px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .header p { font-size: 1.1rem; opacity: 0.9; }
        .section { background: white; padding: 2rem; margin-bottom: 2rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .section h2 { color: #4a5568; margin-bottom: 1rem; font-size: 1.5rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
        .card { background: #f8fafc; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #667eea; }
        .card h3 { color: #2d3748; margin-bottom: 0.5rem; }
        .card p { color: #4a5568; font-size: 0.9rem; }
        .button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; transition: transform 0.2s; }
        .button:hover { transform: translateY(-2px); }
        .form-group { margin-bottom: 1rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; font-weight: 600; color: #4a5568; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px; border: 1px solid #e2e8f0; border-radius: 4px; font-size: 1rem; }
        .status { padding: 1rem; border-radius: 6px; margin: 1rem 0; }
        .status.success { background: #f0fff4; border: 1px solid #68d391; color: #22543d; }
        .status.error { background: #fed7d7; border: 1px solid #fc8181; color: #742a2a; }
        .result-box { background: #edf2f7; padding: 1.5rem; border-radius: 8px; margin-top: 1rem; }
        .metric { display: inline-block; background: white; padding: 1rem; margin: 0.5rem; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); min-width: 150px; text-align: center; }
        .metric-value { font-size: 2rem; font-weight: bold; color: #667eea; }
        .metric-label { font-size: 0.9rem; color: #4a5568; }
        pre { background: #2d3748; color: #e2e8f0; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.9rem; }
        .footer { text-align: center; padding: 2rem; color: #718096; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Governance Platform</h1>
            <p>Enterprise AI Risk Assessment, Bias Detection & Compliance Automation</p>
        </div>

        <div class="section">
            <h2>🎯 Quick Start - AI System Assessment</h2>
            <div class="grid">
                <div class="card">
                    <h3>🚀 Rapid Risk Screening</h3>
                    <p>Fast 30-second risk assessment for AI systems</p>
                    <button class="button" onclick="runRapidAssessment()">Run Rapid Assessment</button>
                </div>
                <div class="card">
                    <h3>🔍 Comprehensive Analysis</h3>
                    <p>Full multi-agent governance evaluation</p>
                    <button class="button" onclick="runComprehensiveAssessment()">Run Full Assessment</button>
                </div>
                <div class="card">
                    <h3>⚖️ Bias Detection</h3>
                    <p>Fairness analysis across protected characteristics</p>
                    <button class="button" onclick="runBiasDetection()">Detect Bias</button>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🛠️ Custom AI System Assessment</h2>
            <form id="assessmentForm">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div class="form-group">
                        <label>System Name</label>
                        <input type="text" id="systemName" value="Test Recommendation System" required>
                    </div>
                    <div class="form-group">
                        <label>System Type</label>
                        <select id="systemType" required>
                            <option value="recommendation_system">Recommendation System</option>
                            <option value="automated_decision_making">Automated Decision Making</option>
                            <option value="risk_assessment">Risk Assessment</option>
                            <option value="fraud_detection">Fraud Detection</option>
                            <option value="content_filtering">Content Filtering</option>
                            <option value="computer_vision">Computer Vision</option>
                            <option value="natural_language_processing">NLP System</option>
                            <option value="medical_ai">Medical AI</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Users Affected</label>
                        <input type="number" id="usersAffected" value="100000" required>
                    </div>
                    <div class="form-group">
                        <label>Business Impact</label>
                        <select id="businessImpact" required>
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                            <option value="critical">Critical</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Decision Automation</label>
                        <select id="decisionAutomation" required>
                            <option value="none">None</option>
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                            <option value="full">Full</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Data Sensitivity</label>
                        <select id="dataSensitivity" required>
                            <option value="public">Public</option>
                            <option value="internal">Internal</option>
                            <option value="confidential">Confidential</option>
                            <option value="personal_data">Personal Data</option>
                            <option value="sensitive_personal">Sensitive Personal</option>
                        </select>
                    </div>
                </div>
                <div class="form-group">
                    <label>System Description</label>
                    <textarea id="description" rows="3" placeholder="Describe the AI system's purpose and functionality">AI-powered recommendation system for e-commerce platform using collaborative filtering and content-based algorithms</textarea>
                </div>
                <button type="submit" class="button">🔍 Assess AI System</button>
            </form>
        </div>

        <div id="results" class="section" style="display: none;">
            <h2>📊 Assessment Results</h2>
            <div id="resultsContent"></div>
        </div>

        <div class="section">
            <h2>📈 Platform Status</h2>
            <div class="grid">
                <div class="card">
                    <h3>🗄️ Database Status</h3>
                    <p id="dbStatus">Loading...</p>
                    <button class="button" onclick="checkStatus()">Refresh Status</button>
                </div>
                <div class="card">
                    <h3>🎭 Orchestrator Health</h3>
                    <p id="orchestratorStatus">Loading...</p>
                    <button class="button" onclick="checkHealth()">Check Health</button>
                </div>
                <div class="card">
                    <h3>🧪 Run Tests</h3>
                    <p>Comprehensive platform testing</p>
                    <button class="button" onclick="runTests()">Run All Tests</button>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>🚀 AI Governance Platform - Enterprise Edition | Built with Flask, Multi-Agent AI & Regulatory Compliance</p>
        </div>
    </div>

    <script>
        // Load initial status
        document.addEventListener('DOMContentLoaded', function() {
            checkStatus();
            checkHealth();
        });

        // Form submission
        document.getElementById('assessmentForm').addEventListener('submit', function(e) {
            e.preventDefault();
            assessCustomSystem();
        });

        function showResults(title, data) {
            const resultsDiv = document.getElementById('results');
            const contentDiv = document.getElementById('resultsContent');

            let html = `<h3>${title}</h3>`;

            if (data.overall_risk_score !== undefined) {
                html += `
                    <div class="metric">
                        <div class="metric-value">${data.overall_risk_score}/10</div>
                        <div class="metric-label">Risk Score</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${data.risk_level || 'N/A'}</div>
                        <div class="metric-label">Risk Level</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${data.confidence_score || 'N/A'}/10</div>
                        <div class="metric-label">Confidence</div>
                    </div>
                `;
            }

            if (data.bias_detected !== undefined) {
                html += `
                    <div class="metric">
                        <div class="metric-value">${data.bias_detected ? 'YES' : 'NO'}</div>
                        <div class="metric-label">Bias Detected</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${data.bias_severity || 'N/A'}</div>
                        <div class="metric-label">Severity</div>
                    </div>
                `;
            }

            html += `<div class="result-box"><pre>${JSON.stringify(data, null, 2)}</pre></div>`;

            contentDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }

        async function runRapidAssessment() {
            const testSystem = {
                system_id: 'DEMO_RAPID_001',
                system_name: 'Demo Recommendation System',
                system_type: 'recommendation_system',
                description: 'Demo AI recommendation system for rapid assessment',
                users_affected: 50000,
                decision_automation: 'medium',
                data_sensitivity: 'personal_data',
                business_impact: 'medium'
            };

            try {
                const response = await fetch('/api/assessment/rapid', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ system_context: testSystem })
                });
                const data = await response.json();
                showResults('🚀 Rapid Assessment Results', data);
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        async function runComprehensiveAssessment() {
            const testSystem = {
                system_id: 'DEMO_COMP_001',
                system_name: 'Demo Fraud Detection System',
                system_type: 'fraud_detection',
                description: 'Demo AI fraud detection system for comprehensive assessment',
                users_affected: 200000,
                decision_automation: 'high',
                data_sensitivity: 'confidential',
                business_impact: 'critical',
                regulatory_scope: ['GDPR', 'PCI_DSS', 'SOX']
            };

            try {
                const response = await fetch('/api/assessment/comprehensive', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ system_context: testSystem })
                });
                const data = await response.json();
                showResults('🔍 Comprehensive Assessment Results', data);
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        async function runBiasDetection() {
            const testSystem = {
                system_id: 'DEMO_BIAS_001',
                system_name: 'Demo Hiring AI System',
                system_type: 'automated_decision_making',
                description: 'Demo AI hiring system for bias detection analysis',
                users_affected: 10000,
                decision_automation: 'high',
                data_sensitivity: 'personal_data',
                business_impact: 'high'
            };

            try {
                const response = await fetch('/api/bias/detect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ system_context: testSystem })
                });
                const data = await response.json();
                showResults('⚖️ Bias Detection Results', data);
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        async function assessCustomSystem() {
            const systemData = {
                system_id: 'CUSTOM_' + Date.now(),
                system_name: document.getElementById('systemName').value,
                system_type: document.getElementById('systemType').value,
                description: document.getElementById('description').value,
                users_affected: parseInt(document.getElementById('usersAffected').value),
                decision_automation: document.getElementById('decisionAutomation').value,
                data_sensitivity: document.getElementById('dataSensitivity').value,
                business_impact: document.getElementById('businessImpact').value,
                deployment_status: 'testing',
                human_oversight: 'moderate'
            };

            try {
                const response = await fetch('/api/assessment/comprehensive', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ system_context: systemData })
                });
                const data = await response.json();
                showResults('🎯 Custom System Assessment', data);
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        async function checkStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                document.getElementById('dbStatus').innerHTML = `
                    ✅ Connected<br>
                    📊 ${data.ai_systems_count} AI Systems<br>
                    📋 ${data.policies_count} Policies
                `;
            } catch (error) {
                document.getElementById('dbStatus').innerHTML = '❌ Connection Error';
            }
        }

        async function checkHealth() {
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                document.getElementById('orchestratorStatus').innerHTML = `
                    ✅ ${data.status}<br>
                    🤖 ${data.healthy_agents}/${data.total_agents} Agents<br>
                    🔄 ${data.active_workflows} Active Workflows
                `;
            } catch (error) {
                document.getElementById('orchestratorStatus').innerHTML = '❌ Health Check Failed';
            }
        }

        async function runTests() {
            try {
                const response = await fetch('/api/test');
                const data = await response.json();
                showResults('🧪 Test Results', data);
            } catch (error) {
                alert('Test Error: ' + error.message);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard for AI Governance Platform"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    """Get platform status"""
    try:
        connection = governance_db.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM ai_systems")
        ai_systems_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM policies")
        policies_count = cursor.fetchone()[0]

        return jsonify({
            'status': 'healthy',
            'ai_systems_count': ai_systems_count,
            'policies_count': policies_count,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/health')
def get_health():
    """Get orchestrator health status"""
    try:
        health = orchestrator.health_check()
        stats = orchestrator.get_orchestrator_stats()

        healthy_agents = sum(1 for status in health.get('agent_health', {}).values() if status)
        total_agents = len(health.get('agent_health', {}))

        return jsonify({
            'status': 'healthy',
            'healthy_agents': healthy_agents,
            'total_agents': total_agents,
            'active_workflows': stats.get('active_workflows', 0),
            'agent_health': health.get('agent_health', {})
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/assessment/rapid', methods=['POST'])
def rapid_assessment():
    """Perform rapid risk screening"""
    try:
        data = request.get_json()
        system_context = data.get('system_context', {})

        result = example_rapid_screening(knowledge_store, governance_db, system_context)

        return jsonify(result)
    except Exception as e:
        logger.error(f"Rapid assessment failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/assessment/comprehensive', methods=['POST'])
def comprehensive_assessment():
    """Perform comprehensive governance assessment"""
    try:
        data = request.get_json()
        system_context = data.get('system_context', {})

        result = example_comprehensive_assessment(knowledge_store, governance_db, system_context)

        return jsonify(result)
    except Exception as e:
        logger.error(f"Comprehensive assessment failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/bias/detect', methods=['POST'])
def detect_bias():
    """Perform bias detection analysis"""
    try:
        data = request.get_json()
        system_context = data.get('system_context', {})

        bias_agent = BiasDetectionAgent(knowledge_store, governance_db)
        result = bias_agent.detect_bias(system_context)

        return jsonify(result)
    except Exception as e:
        logger.error(f"Bias detection failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/risk/assess', methods=['POST'])
def assess_risk():
    """Perform risk assessment"""
    try:
        data = request.get_json()
        system_context = data.get('system_context', {})

        risk_agent = RiskAssessmentAgent(knowledge_store, governance_db)
        result = risk_agent.assess_ai_system_risk(system_context)

        return jsonify(result)
    except Exception as e:
        logger.error(f"Risk assessment failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test')
def run_tests():
    """Run platform tests"""
    try:
        # Import and run test suite
        from test_governance import GovernanceSystemTester

        tester = GovernanceSystemTester()
        # Run a subset of tests for API response
        tester._test_database_connectivity()

        return jsonify({
            'status': 'completed',
            'tests_passed': len([r for r in tester.test_results if r[1] == 'PASSED']),
            'total_tests': len(tester.test_results),
            'results': tester.test_results,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Tests failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/systems')
def get_systems():
    """Get list of AI systems"""
    try:
        connection = governance_db.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT system_id, system_name, system_type, risk_category,
                   deployment_status, governance_score, compliance_status
            FROM ai_systems
            ORDER BY governance_score DESC
            LIMIT 20
        """)

        systems = []
        for row in cursor.fetchall():
            systems.append({
                'system_id': row[0],
                'system_name': row[1],
                'system_type': row[2],
                'risk_category': row[3],
                'deployment_status': row[4],
                'governance_score': row[5],
                'compliance_status': row[6]
            })

        return jsonify({'systems': systems})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("🚀 AI GOVERNANCE PLATFORM - STARTING")
    print("="*60)

    # Initialize platform
    if initialize_governance_platform():
        print("✅ Governance platform initialized successfully")
        print("🌐 Starting Flask web server...")
        print("📱 Access the platform at: http://localhost:5000")
        print("🔗 API endpoints available at: http://localhost:5000/api/")
        print("="*60)

        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to initialize governance platform")
        sys.exit(1)