from flask import Flask, request, jsonify
from agents.liability_protection_agent import LiabilityProtectionAgent, generate_executive_summary
import json
from datetime import datetime

app = Flask(__name__)

# Initialize liability protection agent
liability_agent = LiabilityProtectionAgent()

@app.route('/')
def hello_world():
    return 'AI Governance Platform - Flask backend is running!'

@app.route('/api/governance/liability-analysis', methods=['POST'])
def analyze_liability():
    """Generate CRO liability protection analysis"""
    try:
        data = request.get_json()

        governance_assessment = data.get('governance_assessment', {})
        system_context = data.get('system_context', {})
        decision_maker = data.get('decision_maker', 'Unknown CRO')
        proposed_action = data.get('proposed_action', 'Continue AI system operation')

        # Analyze regulatory consequences
        consequences = liability_agent.analyze_regulatory_consequences(
            governance_assessment, system_context
        )

        # Generate defensible decision documentation
        decision = liability_agent.generate_defensible_decision_doc(
            governance_assessment, system_context, decision_maker, proposed_action
        )

        # Calculate liability exposure
        liability_analysis = liability_agent.calculate_decision_liability_exposure(
            decision, consequences
        )

        # Generate executive summary
        executive_summary = generate_executive_summary(liability_analysis, decision)

        return jsonify({
            'regulatory_consequences': [
                {
                    'regulation': c.regulation,
                    'violation_type': c.violation_type,
                    'financial_penalty_range': f"${c.financial_penalty_min:,.0f} - ${c.financial_penalty_max:,.0f}",
                    'criminal_liability_risk': c.criminal_liability_risk,
                    'timeline_to_enforcement': c.timeline_to_enforcement,
                    'precedent_cases': c.precedent_cases
                }
                for c in consequences
            ],
            'defensible_decision': {
                'decision_id': decision.decision_id,
                'defensibility_score': liability_analysis['defensibility_score'],
                'recommendation': liability_analysis['recommendation'],
                'board_approval_required': decision.board_approval_required,
                'legal_review_completed': decision.legal_review_completed,
                'risk_acceptance_justification': decision.risk_acceptance_justification,
                'mitigation_measures': decision.mitigation_measures_implemented,
                'expert_consultations': decision.expert_consultation_record
            },
            'liability_exposure': liability_analysis,
            'executive_summary': executive_summary,
            'generated_at': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': f'Liability analysis failed: {str(e)}'}), 500

@app.route('/api/governance/executive-decision', methods=['POST'])
def generate_executive_decision():
    """Generate executive decision package for C-suite approval"""
    try:
        data = request.get_json()

        # Sample governance assessment for demo
        sample_assessment = {
            'governance_score': 72.5,
            'risk_assessment': {
                'overall_risk_level': 'high',
                'risk_score': 7.2
            },
            'compliance_analysis': {
                'regulatory_frameworks': {
                    'EU_AI_Act': {'compliance_percentage': 65},
                    'GDPR_AI': {'compliance_percentage': 85}
                }
            },
            'bias_evaluation': {
                'bias_risk_level': 'medium'
            }
        }

        system_context = {
            'system_name': data.get('system_name', 'Credit Scoring AI'),
            'business_unit': 'Financial Services',
            'annual_revenue': 15_000_000,
            'company_global_revenue': 2_000_000_000,
            'deployment_status': 'production'
        }

        decision_maker = data.get('decision_maker', 'Chief Risk Officer')

        # Generate comprehensive liability analysis
        consequences = liability_agent.analyze_regulatory_consequences(
            sample_assessment, system_context
        )

        decision = liability_agent.generate_defensible_decision_doc(
            sample_assessment, system_context, decision_maker,
            'Continue operation with enhanced monitoring'
        )

        liability_analysis = liability_agent.calculate_decision_liability_exposure(
            decision, consequences
        )

        executive_summary = generate_executive_summary(liability_analysis, decision)

        # Create comprehensive decision package
        decision_package = {
            'executive_summary': executive_summary,
            'decision_recommendation': liability_analysis['recommendation'],
            'financial_impact': {
                'system_annual_revenue': f"${system_context['annual_revenue']:,}",
                'max_regulatory_penalty': f"${liability_analysis['total_regulatory_exposure']['maximum']:,.0f}",
                'risk_adjusted_cost': f"${liability_analysis['total_regulatory_exposure']['risk_adjusted']:,.0f}",
                'insurance_gap': f"${liability_analysis['insurance_protection']['estimated_gap']:,.0f}"
            },
            'legal_defensibility': {
                'score': f"{liability_analysis['defensibility_score']:.0f}/100",
                'status': 'Strong' if liability_analysis['defensibility_score'] >= 80 else 'Moderate' if liability_analysis['defensibility_score'] >= 60 else 'Weak',
                'board_approval_required': decision.board_approval_required
            },
            'regulatory_risks': [
                {
                    'framework': c.regulation,
                    'max_penalty': f"${c.financial_penalty_max:,.0f}",
                    'enforcement_timeline': c.timeline_to_enforcement,
                    'precedents': c.precedent_cases[:2]  # Top 2 precedents
                }
                for c in consequences
            ],
            'next_steps': [
                'Board resolution required' if decision.board_approval_required else 'Proceed with enhanced monitoring',
                'Implement weekly bias detection reports',
                'Schedule quarterly external compliance audits',
                'Maintain D&O insurance coverage verification',
                'Establish proactive regulator communication plan'
            ],
            'decision_id': decision.decision_id,
            'generated_for': decision_maker,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        }

        return jsonify(decision_package)

    except Exception as e:
        return jsonify({'error': f'Executive decision generation failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
