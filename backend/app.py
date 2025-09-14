#!/usr/bin/env python3
"""
AI Governance Pod - Main Flask Application
Provides REST API for AI system governance, risk assessment, and compliance monitoring
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import json

# Import our custom modules
from agents.risk_agent import RiskAgent
from agents.policy_agent import PolicyAgent
from agents.bias_agent import BiasAgent
from agents.audit_agent import AuditAgent
from database.chromadb_manager import GovernanceKnowledgeStore
from database.sqlite_manager import GovernanceDataManager
from utils.security import GovernanceSecurityManager
from utils.monitoring import GovernanceMonitoring

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'governance-secret-key-change-in-production')
CORS(app, supports_credentials=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/governance_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize system components
try:
    # Database managers
    knowledge_store = GovernanceKnowledgeStore()
    governance_db = GovernanceDataManager()
    
    # Security and monitoring
    security_manager = GovernanceSecurityManager()
    monitoring = GovernanceMonitoring()
    
    # AI Agents
    risk_agent = RiskAgent(knowledge_store, governance_db)
    policy_agent = PolicyAgent(knowledge_store, governance_db)
    bias_agent = BiasAgent(knowledge_store, governance_db)
    audit_agent = AuditAgent(knowledge_store, governance_db)
    
    logger.info("All AI governance system components initialized successfully")
    
except Exception as e:
    logger.error(f"Failed to initialize system components: {str(e)}")
    raise

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connections
        knowledge_store.health_check()
        governance_db.health_check()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'components': {
                'database': 'ok',
                'agents': 'ok',
                'security': 'ok',
                'compliance': 'ok'
            }
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/governance/start-assessment', methods=['POST'])
def start_governance_assessment():
    """Initialize a new AI system governance assessment"""
    try:
        data = request.get_json()
        system_id = data.get('system_id')
        assessor_id = data.get('assessor_id')
        
        if not system_id or not assessor_id:
            return jsonify({'error': 'System ID and Assessor ID required'}), 400
        
        # Create secure assessment session
        session_data = security_manager.create_governance_session(system_id, assessor_id)
        session['system_id'] = system_id
        session['assessor_id'] = assessor_id
        session['session_token'] = session_data['token']
        
        # Log assessment start for compliance
        security_manager.log_governance_access(
            system_id=system_id,
            assessor_id=assessor_id,
            action='assessment_start',
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'session_id': session_data['session_id'],
            'system_id': system_id,
            'assessor_id': assessor_id,
            'message': 'Governance assessment session started successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to start governance assessment: {str(e)}")
        return jsonify({'error': 'Failed to start assessment'}), 500

@app.route('/api/governance/assess-system', methods=['POST'])
def assess_ai_system():
    """Comprehensive AI system governance assessment"""
    try:
        data = request.get_json()
        system_id = session.get('system_id')
        assessor_id = session.get('assessor_id')
        assessment_request = data.get('assessment_request', '')
        system_context = data.get('system_context', {})
        
        if not system_id or not assessor_id:
            return jsonify({'error': 'No active assessment session'}), 401
        
        if not assessment_request:
            return jsonify({'error': 'Assessment request is required'}), 400
        
        # Security: Encrypt and audit log the assessment
        encrypted_request = security_manager.encrypt_governance_data(assessment_request)
        security_manager.log_governance_interaction(
            system_id=system_id,
            assessor_id=assessor_id,
            request=assessment_request,
            ip_address=request.remote_addr
        )
        
        # Step 1: Risk Agent evaluates AI system risks
        risk_assessment = risk_agent.assess_system_risks(
            system_id=system_id,
            assessment_request=assessment_request,
            system_context=system_context
        )
        
        # Step 2: Policy Agent checks compliance
        compliance_result = policy_agent.check_policy_compliance(
            system_id=system_id,
            system_context=system_context,
            risk_factors=risk_assessment['identified_risks']
        )
        
        # Step 3: Bias Agent evaluates fairness
        bias_analysis = bias_agent.analyze_system_bias(
            system_id=system_id,
            system_context=system_context,
            risk_assessment=risk_assessment
        )
        
        # Step 4: Audit Agent documents findings
        audit_documentation = audit_agent.document_assessment(
            system_id=system_id,
            risk_assessment=risk_assessment,
            compliance_result=compliance_result,
            bias_analysis=bias_analysis,
            assessor_id=assessor_id
        )
        
        # Calculate overall governance score
        governance_score = calculate_governance_score(
            risk_assessment, compliance_result, bias_analysis
        )
        
        # Prepare comprehensive response
        response = {
            'system_id': system_id,
            'governance_score': governance_score,
            'risk_assessment': {
                'overall_risk_level': risk_assessment['risk_level'],
                'risk_score': risk_assessment['risk_score'],
                'identified_risks': risk_assessment['identified_risks'],
                'mitigation_recommendations': risk_assessment['mitigation_recommendations']
            },
            'compliance_analysis': {
                'compliance_status': compliance_result['status'],
                'regulatory_frameworks': compliance_result['frameworks'],
                'compliance_gaps': compliance_result['gaps'],
                'remediation_actions': compliance_result['remediation_actions']
            },
            'bias_evaluation': {
                'bias_risk_level': bias_analysis['bias_level'],
                'fairness_metrics': bias_analysis['fairness_metrics'],
                'bias_mitigation': bias_analysis['mitigation_strategies']
            },
            'audit_trail': audit_documentation,
            'assessment_summary': generate_executive_summary(
                governance_score, risk_assessment, compliance_result, bias_analysis
            ),
            'next_actions': determine_next_actions(governance_score, compliance_result),
            'assessment_id': audit_documentation['assessment_id'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Store assessment in database
        governance_db.store_assessment(
            system_id=system_id,
            assessment_id=response['assessment_id'],
            assessor_id=assessor_id,
            assessment_data=response,
            governance_score=governance_score
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Failed to assess AI system: {str(e)}")
        return jsonify({'error': 'Failed to complete assessment'}), 500

@app.route('/api/governance/system-history', methods=['GET'])
def get_system_governance_history():
    """Retrieve AI system's governance assessment history"""
    try:
        system_id = session.get('system_id')
        assessor_id = session.get('assessor_id')
        
        if not system_id or not assessor_id:
            return jsonify({'error': 'No active assessment session'}), 401
        
        # Security check
        if not security_manager.verify_governance_access(system_id, assessor_id, session.get('session_token')):
            return jsonify({'error': 'Unauthorized access'}), 403
        
        # Retrieve assessment history
        history = governance_db.get_system_history(system_id)
        
        # Decrypt sensitive data
        decrypted_history = security_manager.decrypt_assessment_history(history)
        
        return jsonify({
            'system_id': system_id,
            'assessments': decrypted_history,
            'total_assessments': len(decrypted_history),
            'governance_trend': analyze_governance_trend(decrypted_history)
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to retrieve system governance history: {str(e)}")
        return jsonify({'error': 'Failed to retrieve history'}), 500

@app.route('/api/governance/dashboard', methods=['GET'])
def get_governance_dashboard():
    """Get governance dashboard data for risk officers"""
    try:
        # This would require proper role-based authentication in production
        dashboard_data = monitoring.get_governance_dashboard_data()
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        logger.error(f"Failed to retrieve governance dashboard: {str(e)}")
        return jsonify({'error': 'Failed to retrieve dashboard'}), 500

@app.route('/api/governance/compliance-report', methods=['POST'])
def generate_compliance_report():
    """Generate comprehensive compliance report"""
    try:
        data = request.get_json()
        report_scope = data.get('scope', 'enterprise')
        frameworks = data.get('frameworks', ['EU_AI_Act', 'NIST_AI_RMF'])
        
        # Generate comprehensive compliance report
        report = audit_agent.generate_compliance_report(
            scope=report_scope,
            regulatory_frameworks=frameworks,
            assessor_id=session.get('assessor_id')
        )
        
        return jsonify(report), 200
        
    except Exception as e:
        logger.error(f"Failed to generate compliance report: {str(e)}")
        return jsonify({'error': 'Failed to generate report'}), 500

@app.route('/api/governance/policy-search', methods=['POST'])
def search_governance_policies():
    """Search governance policy knowledge base"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        policy_type = data.get('policy_type', 'all')
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        results = policy_agent.search_policy_knowledge(query, policy_type)
        
        return jsonify({
            'query': query,
            'policy_type': policy_type,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to search policy knowledge: {str(e)}")
        return jsonify({'error': 'Policy search failed'}), 500

@app.route('/api/governance/risk-monitoring', methods=['POST'])
def monitor_system_risks():
    """Real-time AI system risk monitoring"""
    try:
        data = request.get_json()
        system_id = data.get('system_id')
        monitoring_parameters = data.get('parameters', {})
        
        if not system_id:
            return jsonify({'error': 'System ID is required'}), 400
        
        monitoring_result = risk_agent.monitor_system_risks(
            system_id=system_id,
            monitoring_parameters=monitoring_parameters
        )
        
        return jsonify({
            'system_id': system_id,
            'monitoring_result': monitoring_result,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to monitor system risks: {str(e)}")
        return jsonify({'error': 'Risk monitoring failed'}), 500

@app.route('/api/admin/governance-metrics', methods=['GET'])
def get_governance_metrics():
    """Get system-wide governance metrics for administrators"""
    try:
        # This would require admin authentication in production
        metrics = monitoring.get_governance_metrics()
        
        return jsonify(metrics), 200
        
    except Exception as e:
        logger.error(f"Failed to retrieve governance metrics: {str(e)}")
        return jsonify({'error': 'Failed to retrieve metrics'}), 500

# Helper functions

def calculate_governance_score(risk_assessment, compliance_result, bias_analysis):
    """Calculate overall governance score (0-100)"""
    try:
        # Weight the different components
        risk_weight = 0.4
        compliance_weight = 0.35
        bias_weight = 0.25
        
        # Normalize scores to 0-100 scale
        risk_score = max(0, 100 - (risk_assessment['risk_score'] * 10))
        compliance_score = compliance_result['compliance_percentage']
        bias_score = max(0, 100 - (bias_analysis.get('bias_risk_score', 5) * 10))
        
        overall_score = (
            risk_score * risk_weight +
            compliance_score * compliance_weight +
            bias_score * bias_weight
        )
        
        return round(overall_score, 1)
        
    except Exception as e:
        logger.error(f"Failed to calculate governance score: {str(e)}")
        return 50  # Default middle score

def generate_executive_summary(governance_score, risk_assessment, compliance_result, bias_analysis):
    """Generate executive summary of governance assessment"""
    try:
        if governance_score >= 85:
            status = "Excellent governance posture with minimal risks"
        elif governance_score >= 70:
            status = "Good governance with some areas for improvement"
        elif governance_score >= 50:
            status = "Moderate governance concerns requiring attention"
        else:
            status = "Significant governance issues requiring immediate action"
        
        return {
            'overall_status': status,
            'governance_score': governance_score,
            'key_findings': [
                f"Risk Level: {risk_assessment['risk_level']}",
                f"Compliance Status: {compliance_result['status']}",
                f"Bias Risk: {bias_analysis['bias_level']}"
            ],
            'priority_actions': compliance_result.get('remediation_actions', [])[:3]
        }
        
    except Exception as e:
        logger.error(f"Failed to generate executive summary: {str(e)}")
        return {'overall_status': 'Assessment incomplete', 'governance_score': 0}

def determine_next_actions(governance_score, compliance_result):
    """Determine recommended next actions based on assessment"""
    try:
        actions = []
        
        if governance_score < 50:
            actions.append({
                'priority': 'high',
                'action': 'Immediate governance review required',
                'description': 'Schedule emergency governance committee review'
            })
        
        if compliance_result.get('gaps'):
            actions.append({
                'priority': 'medium',
                'action': 'Address compliance gaps',
                'description': f"Resolve {len(compliance_result['gaps'])} identified compliance issues"
            })
        
        if governance_score >= 85:
            actions.append({
                'priority': 'low',
                'action': 'Continue monitoring',
                'description': 'Maintain current governance practices with regular reviews'
            })
        
        return actions
        
    except Exception as e:
        logger.error(f"Failed to determine next actions: {str(e)}")
        return []

def analyze_governance_trend(assessment_history):
    """Analyze governance score trend over time"""
    try:
        if len(assessment_history) < 2:
            return {'trend': 'insufficient_data'}
        
        scores = [assessment.get('governance_score', 50) for assessment in assessment_history[-5:]]
        
        if len(scores) >= 2:
            if scores[-1] > scores[-2]:
                trend = 'improving'
            elif scores[-1] < scores[-2]:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'current_score': scores[-1] if scores else 50,
            'score_history': scores
        }
        
    except Exception as e:
        logger.error(f"Failed to analyze governance trend: {str(e)}")
        return {'trend': 'unknown'}

# Error handlers

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

# Application startup

if __name__ == '__main__':
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Start the Flask application
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5001))  # Different port from Pod1
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting AI Governance Pod on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )