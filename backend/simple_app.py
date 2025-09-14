from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'governance_data.db')

# Simple HTML interface
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Governance Platform</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
        .stats { display: flex; justify-content: space-around; margin: 20px 0; }
        .stat-box { background: #3498db; color: white; padding: 15px; border-radius: 5px; text-align: center; min-width: 120px; }
        .stat-number { font-size: 24px; font-weight: bold; }
        .stat-label { font-size: 12px; }
        button { background: #2c3e50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        button:hover { background: #34495e; }
        .results { margin-top: 20px; padding: 15px; background: #ecf0f1; border-radius: 5px; white-space: pre-wrap; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #3498db; color: white; }
        .risk-high { background-color: #e74c3c; color: white; }
        .risk-medium { background-color: #f39c12; color: white; }
        .risk-low { background-color: #27ae60; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ AI Governance Platform</h1>

        <div class="stats" id="stats">
            <div class="stat-box">
                <div class="stat-number" id="totalSystems">-</div>
                <div class="stat-label">AI Systems</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="highRiskSystems">-</div>
                <div class="stat-label">High Risk</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="totalAssessments">-</div>
                <div class="stat-label">Assessments</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="complianceScore">-</div>
                <div class="stat-label">Avg Compliance</div>
            </div>
        </div>

        <div style="text-align: center; margin: 20px 0;">
            <button onclick="loadStats()">📊 Load Platform Statistics</button>
            <button onclick="loadSystems()">🤖 View AI Systems</button>
            <button onclick="loadRiskAssessments()">⚠️ Risk Assessments</button>
            <button onclick="loadBiasEvaluations()">🎯 Bias Evaluations</button>
            <button onclick="runSimpleAssessment()">🔍 Quick Assessment</button>
        </div>

        <div id="results" class="results" style="display: none;"></div>
    </div>

    <script>
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();

                document.getElementById('totalSystems').textContent = data.total_systems;
                document.getElementById('highRiskSystems').textContent = data.high_risk_systems;
                document.getElementById('totalAssessments').textContent = data.total_assessments;
                document.getElementById('complianceScore').textContent = data.avg_compliance + '%';

                showResults('Platform statistics loaded successfully!');
            } catch (error) {
                showResults('Error loading stats: ' + error.message);
            }
        }

        async function loadSystems() {
            try {
                const response = await fetch('/api/systems');
                const systems = await response.json();

                let html = '<table><tr><th>System Name</th><th>Type</th><th>Risk Category</th><th>Status</th><th>Governance Score</th></tr>';
                systems.slice(0, 10).forEach(system => {
                    const riskClass = system.risk_category === 'high' ? 'risk-high' :
                                     system.risk_category === 'medium' ? 'risk-medium' : 'risk-low';
                    html += `<tr>
                        <td>${system.system_name}</td>
                        <td>${system.system_type}</td>
                        <td class="${riskClass}">${system.risk_category}</td>
                        <td>${system.deployment_status}</td>
                        <td>${system.governance_score || 'N/A'}</td>
                    </tr>`;
                });
                html += '</table>';

                showResults(html);
            } catch (error) {
                showResults('Error loading systems: ' + error.message);
            }
        }

        async function loadRiskAssessments() {
            try {
                const response = await fetch('/api/risk-assessments');
                const assessments = await response.json();

                let html = '<table><tr><th>System ID</th><th>Assessment Date</th><th>Overall Risk</th><th>Bias Risk</th><th>Privacy Risk</th></tr>';
                assessments.slice(0, 10).forEach(assessment => {
                    html += `<tr>
                        <td>${assessment.system_id.substring(0, 8)}...</td>
                        <td>${new Date(assessment.assessment_date).toLocaleDateString()}</td>
                        <td>${assessment.overall_risk_score}/10</td>
                        <td>${assessment.bias_risk_score}/10</td>
                        <td>${assessment.privacy_risk_score}/10</td>
                    </tr>`;
                });
                html += '</table>';

                showResults(html);
            } catch (error) {
                showResults('Error loading risk assessments: ' + error.message);
            }
        }

        async function loadBiasEvaluations() {
            try {
                const response = await fetch('/api/bias-evaluations');
                const evaluations = await response.json();

                let html = '<table><tr><th>System ID</th><th>Evaluation Date</th><th>Bias Detected</th><th>Severity</th><th>Affected Groups</th></tr>';
                evaluations.forEach(evaluation => {
                    const affectedGroups = JSON.parse(evaluation.affected_groups || '[]').join(', ');
                    html += `<tr>
                        <td>${evaluation.system_id.substring(0, 8)}...</td>
                        <td>${new Date(evaluation.evaluation_date).toLocaleDateString()}</td>
                        <td>${evaluation.bias_detected ? 'Yes' : 'No'}</td>
                        <td>${evaluation.bias_severity}</td>
                        <td>${affectedGroups}</td>
                    </tr>`;
                });
                html += '</table>';

                showResults(html);
            } catch (error) {
                showResults('Error loading bias evaluations: ' + error.message);
            }
        }

        async function runSimpleAssessment() {
            try {
                const response = await fetch('/api/simple-assessment', { method: 'POST' });
                const result = await response.json();

                const html = `
Assessment Results:
==================
System: ${result.system_name}
Overall Risk Score: ${result.risk_score}/10
Compliance Score: ${result.compliance_score}/10
Recommendation: ${result.recommendation}

Risk Breakdown:
- Bias Risk: ${result.bias_risk}/10
- Privacy Risk: ${result.privacy_risk}/10
- Security Risk: ${result.security_risk}/10

Generated at: ${result.timestamp}
                `;

                showResults(html);
            } catch (error) {
                showResults('Error running assessment: ' + error.message);
            }
        }

        function showResults(content) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = content;
            resultsDiv.style.display = 'block';
        }

        // Load stats on page load
        window.onload = loadStats;
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_INTERFACE)

@app.route('/api/stats')
def get_stats():
    """Get platform statistics"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Get total systems
        cursor.execute("SELECT COUNT(*) FROM ai_systems")
        total_systems = cursor.fetchone()[0]

        # Get high risk systems
        cursor.execute("SELECT COUNT(*) FROM ai_systems WHERE risk_category = 'high'")
        high_risk_systems = cursor.fetchone()[0]

        # Get total assessments
        cursor.execute("SELECT COUNT(*) FROM risk_assessments")
        total_assessments = cursor.fetchone()[0]

        # Get average governance score
        cursor.execute("SELECT AVG(governance_score) FROM ai_systems WHERE governance_score IS NOT NULL")
        avg_compliance = cursor.fetchone()[0] or 0

        conn.close()

        return jsonify({
            'total_systems': total_systems,
            'high_risk_systems': high_risk_systems,
            'total_assessments': total_assessments,
            'avg_compliance': round(avg_compliance * 10) if avg_compliance else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/systems')
def get_systems():
    """Get AI systems list"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT system_id, system_name, system_type, risk_category,
                   deployment_status, governance_score
            FROM ai_systems
            ORDER BY created_at DESC
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
                'governance_score': row[5]
            })

        conn.close()
        return jsonify(systems)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/risk-assessments')
def get_risk_assessments():
    """Get risk assessments"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT system_id, assessment_date, overall_risk_score,
                   bias_risk_score, privacy_risk_score, security_risk_score
            FROM risk_assessments
            ORDER BY assessment_date DESC
            LIMIT 20
        """)

        assessments = []
        for row in cursor.fetchall():
            assessments.append({
                'system_id': row[0],
                'assessment_date': row[1],
                'overall_risk_score': row[2],
                'bias_risk_score': row[3],
                'privacy_risk_score': row[4],
                'security_risk_score': row[5]
            })

        conn.close()
        return jsonify(assessments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bias-evaluations')
def get_bias_evaluations():
    """Get bias evaluations"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT system_id, evaluation_date, bias_detected, bias_severity, affected_groups
            FROM bias_evaluations
            ORDER BY evaluation_date DESC
            LIMIT 10
        """)

        evaluations = []
        for row in cursor.fetchall():
            evaluations.append({
                'system_id': row[0],
                'evaluation_date': row[1],
                'bias_detected': bool(row[2]),
                'bias_severity': row[3],
                'affected_groups': row[4]
            })

        conn.close()
        return jsonify(evaluations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/simple-assessment', methods=['POST'])
def simple_assessment():
    """Run a simple governance assessment simulation"""
    try:
        # Get a random system from database
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT system_name, system_type, risk_category
            FROM ai_systems
            ORDER BY RANDOM()
            LIMIT 1
        """)

        system = cursor.fetchone()
        conn.close()

        if not system:
            return jsonify({'error': 'No systems found in database'}), 404

        # Simulate assessment scores
        import random

        risk_score = random.uniform(3.0, 8.5)
        bias_risk = random.uniform(2.0, 7.0)
        privacy_risk = random.uniform(3.0, 8.0)
        security_risk = random.uniform(4.0, 7.5)
        compliance_score = random.uniform(6.0, 9.0)

        # Generate recommendation
        if risk_score >= 7:
            recommendation = "Immediate review required - High risk identified"
        elif risk_score >= 5:
            recommendation = "Enhanced monitoring recommended"
        else:
            recommendation = "Continue with standard governance procedures"

        return jsonify({
            'system_name': system[0],
            'system_type': system[1],
            'risk_category': system[2],
            'risk_score': round(risk_score, 1),
            'bias_risk': round(bias_risk, 1),
            'privacy_risk': round(privacy_risk, 1),
            'security_risk': round(security_risk, 1),
            'compliance_score': round(compliance_score, 1),
            'recommendation': recommendation,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🛡️ Starting AI Governance Platform...")
    print("📊 Database:", DATABASE_PATH)
    print("🌐 Access at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)