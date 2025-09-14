#!/usr/bin/env python3
"""
Risk Assessment Agent for AI Governance
Evaluates AI systems for comprehensive governance risks across multiple dimensions
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from .base_agent import BaseGovernanceAgent

logger = logging.getLogger(__name__)

class RiskAssessmentAgent(BaseGovernanceAgent):
    """
    Evaluates AI systems for governance risks across multiple dimensions
    - Automated risk scoring across bias, privacy, security, explainability, and regulatory compliance
    - Multi-dimensional risk analysis with weighted scoring
    - Regulatory framework mapping and compliance assessment
    - Actionable risk mitigation recommendations
    """

    def __init__(self, knowledge_store, governance_db):
        """Initialize risk assessment agent"""
        super().__init__(knowledge_store, governance_db, "risk_assessment")

        # Risk assessment criteria and weights
        self.risk_dimensions = {
            'bias_fairness': 0.25,
            'privacy_security': 0.25,
            'explainability': 0.20,
            'regulatory_compliance': 0.20,
            'operational_risk': 0.10
        }

        # Risk level thresholds
        self.risk_thresholds = {
            'critical': 8.5,
            'high': 7.0,
            'medium': 4.0,
            'low': 0.0
        }

    def assess_ai_system_risk(self, system_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive risk assessment for an AI system

        Args:
            system_context: Complete AI system information including technical specs,
                          deployment context, data usage, and regulatory scope

        Returns:
            Comprehensive risk assessment with scores, findings, and recommendations
        """
        try:
            assessment_start = datetime.now()

            # Validate input
            if not self._validate_governance_input(['system_id', 'system_name', 'system_type'], system_context):
                raise ValueError("Missing required system information for risk assessment")

            # Generate comprehensive risk assessment prompt
            risk_prompt = self._create_risk_assessment_prompt(system_context)

            # Get AI-powered risk analysis
            risk_analysis = self._generate_governance_response(risk_prompt, system_context)

            # Extract structured risk data
            structured_risk = self._extract_governance_data(risk_analysis, "risk_assessment")

            # Calculate dimensional risk scores
            dimensional_scores = self._calculate_dimensional_risks(system_context, structured_risk)

            # Calculate overall risk score
            overall_risk = self._calculate_overall_risk_score(dimensional_scores)

            # Determine risk level
            risk_level = self._determine_risk_level(overall_risk)

            # Generate regulatory compliance assessment
            regulatory_assessment = self._assess_regulatory_compliance(system_context, dimensional_scores)

            # Generate mitigation recommendations
            recommendations = self._generate_risk_mitigation_recommendations(
                dimensional_scores, regulatory_assessment, system_context
            )

            # Calculate processing time
            processing_time = (datetime.now() - assessment_start).total_seconds()

            # Create assessment result
            assessment_result = {
                'assessment_id': self._create_assessment_id(),
                'system_id': system_context['system_id'],
                'assessment_date': datetime.now().isoformat(),
                'overall_risk_score': round(overall_risk, 2),
                'risk_level': risk_level,
                'dimensional_scores': dimensional_scores,
                'regulatory_assessment': regulatory_assessment,
                'risk_factors': structured_risk.get('risk_factors', []),
                'recommendations': recommendations,
                'confidence_score': structured_risk.get('confidence_level', 7),
                'methodology': 'multi_dimensional_ai_assessment',
                'processing_time_seconds': round(processing_time, 2),
                'requires_review': overall_risk >= self.risk_thresholds['high'],
                'assessment_summary': self._generate_assessment_summary(overall_risk, risk_level, dimensional_scores)
            }

            # Log assessment interaction
            self._log_governance_interaction(
                system_context['system_id'],
                'risk_assessment',
                {'input_context': system_context},
                assessment_result,
                processing_time
            )

            return self._format_governance_response(risk_analysis, assessment_result)

        except Exception as e:
            logger.error(f"Risk assessment failed for system {system_context.get('system_id', 'unknown')}: {str(e)}")
            return self._format_governance_response(
                f"Risk assessment failed due to technical error: {str(e)}",
                {'assessment_status': 'failed', 'error': str(e)}
            )

    def _create_risk_assessment_prompt(self, system_context: Dict[str, Any]) -> str:
        """Create specialized risk assessment prompt"""

        specific_instructions = f"""
RISK ASSESSMENT MISSION:
You are conducting a comprehensive AI governance risk assessment for: {system_context['system_name']}

SYSTEM CONTEXT:
- Type: {system_context.get('system_type', 'Unknown')}
- Deployment: {system_context.get('deployment_status', 'Unknown')}
- Users Affected: {system_context.get('users_affected', 'Unknown')}
- Data Sensitivity: {system_context.get('data_sensitivity', 'Unknown')}
- Decision Automation: {system_context.get('decision_automation', 'Unknown')}
- Human Oversight: {system_context.get('human_oversight', 'Unknown')}
- Business Impact: {system_context.get('business_impact', 'Unknown')}
- Regulatory Scope: {system_context.get('regulatory_scope', [])}

RISK ASSESSMENT FRAMEWORK:
Evaluate and score (1-10 scale) across these critical dimensions:

1. BIAS & FAIRNESS RISK (Weight: 25%)
   - Assess potential for discriminatory outcomes
   - Evaluate fairness across protected characteristics
   - Consider algorithmic bias and representation bias
   - Score based on data sources, model type, and use case

2. PRIVACY & SECURITY RISK (Weight: 25%)
   - Evaluate data protection and privacy risks
   - Assess security vulnerabilities and attack vectors
   - Consider data retention, access controls, and encryption
   - Analyze cross-border data transfer implications

3. EXPLAINABILITY RISK (Weight: 20%)
   - Assess model transparency and interpretability
   - Evaluate explanation quality for decision subjects
   - Consider regulatory requirements for explainability
   - Score based on model complexity and use case criticality

4. REGULATORY COMPLIANCE RISK (Weight: 20%)
   - Map applicable regulatory frameworks
   - Assess compliance with EU AI Act, NIST AI RMF, GDPR
   - Evaluate sector-specific regulations
   - Consider geographic jurisdiction requirements

5. OPERATIONAL RISK (Weight: 10%)
   - Assess system reliability and performance risks
   - Evaluate monitoring and incident response capabilities
   - Consider business continuity and disaster recovery
   - Analyze technical debt and maintenance risks

RISK ANALYSIS REQUIREMENTS:
- Provide specific risk scores (1-10) for each dimension
- Identify concrete risk factors and their severity
- Map applicable regulatory requirements
- Generate actionable mitigation recommendations
- Assess overall confidence level in assessment (1-10)
- Consider system lifecycle stage and deployment context

REGULATORY FRAMEWORK MAPPING:
Specifically analyze compliance with:
- EU AI Act (risk categorization, prohibited practices, high-risk system requirements)
- NIST AI Risk Management Framework (trustworthiness characteristics)
- GDPR (automated decision-making, data subject rights)
- Sector-specific regulations based on use case

OUTPUT REQUIREMENTS:
Provide comprehensive risk analysis including:
1. Dimensional risk scores with justification
2. Identified risk factors and their impact
3. Regulatory compliance gaps and requirements
4. Prioritized mitigation recommendations
5. Overall risk level determination
6. Confidence assessment and limitations

Focus on practical, implementable recommendations that address identified risks while maintaining system effectiveness.
"""

        return self._create_governance_prompt(specific_instructions)

    def _calculate_dimensional_risks(self, system_context: Dict[str, Any],
                                   ai_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk scores for each dimension using AI analysis and system context"""

        dimensional_scores = {}

        # Bias & Fairness Risk
        bias_score = self._calculate_bias_risk(system_context, ai_analysis)
        dimensional_scores['bias_fairness'] = {
            'score': bias_score,
            'weight': self.risk_dimensions['bias_fairness'],
            'factors': self._get_bias_risk_factors(system_context, ai_analysis),
            'assessment_basis': 'AI analysis + system characteristics'
        }

        # Privacy & Security Risk
        privacy_score = self._calculate_privacy_security_risk(system_context, ai_analysis)
        dimensional_scores['privacy_security'] = {
            'score': privacy_score,
            'weight': self.risk_dimensions['privacy_security'],
            'factors': self._get_privacy_security_factors(system_context, ai_analysis),
            'assessment_basis': 'Data sensitivity + security controls'
        }

        # Explainability Risk
        explainability_score = self._calculate_explainability_risk(system_context, ai_analysis)
        dimensional_scores['explainability'] = {
            'score': explainability_score,
            'weight': self.risk_dimensions['explainability'],
            'factors': self._get_explainability_factors(system_context, ai_analysis),
            'assessment_basis': 'Model complexity + use case requirements'
        }

        # Regulatory Compliance Risk
        regulatory_score = self._calculate_regulatory_risk(system_context, ai_analysis)
        dimensional_scores['regulatory_compliance'] = {
            'score': regulatory_score,
            'weight': self.risk_dimensions['regulatory_compliance'],
            'factors': self._get_regulatory_factors(system_context, ai_analysis),
            'assessment_basis': 'Regulatory mapping + compliance gaps'
        }

        # Operational Risk
        operational_score = self._calculate_operational_risk(system_context, ai_analysis)
        dimensional_scores['operational_risk'] = {
            'score': operational_score,
            'weight': self.risk_dimensions['operational_risk'],
            'factors': self._get_operational_factors(system_context, ai_analysis),
            'assessment_basis': 'System reliability + monitoring capabilities'
        }

        return dimensional_scores

    def _calculate_bias_risk(self, system_context: Dict[str, Any], ai_analysis: Dict[str, Any]) -> float:
        """Calculate bias and fairness risk score"""
        base_score = 3.0  # Default medium-low risk

        # Increase risk based on system characteristics
        system_type = system_context.get('system_type', '')
        if system_type in ['automated_decision_making', 'hiring_systems', 'credit_assessment']:
            base_score += 3.0
        elif system_type in ['recommendation_system', 'content_filtering']:
            base_score += 2.0

        # Data sensitivity impact
        data_sensitivity = system_context.get('data_sensitivity', '')
        if data_sensitivity in ['personal_data', 'sensitive_personal']:
            base_score += 1.5

        # Users affected impact
        users_affected = system_context.get('users_affected', 0)
        if users_affected > 100000:
            base_score += 1.0
        elif users_affected > 10000:
            base_score += 0.5

        # Decision automation level
        automation = system_context.get('decision_automation', '')
        if automation in ['high', 'full']:
            base_score += 1.5
        elif automation == 'medium':
            base_score += 0.5

        # Human oversight level (inverse relationship)
        oversight = system_context.get('human_oversight', '')
        if oversight in ['none', 'limited']:
            base_score += 1.0
        elif oversight == 'moderate':
            base_score += 0.3

        return min(10.0, max(1.0, base_score))

    def _calculate_privacy_security_risk(self, system_context: Dict[str, Any], ai_analysis: Dict[str, Any]) -> float:
        """Calculate privacy and security risk score"""
        base_score = 2.0  # Default low risk

        # Data sensitivity is primary factor
        data_sensitivity = system_context.get('data_sensitivity', '')
        if data_sensitivity == 'sensitive_personal':
            base_score += 4.0
        elif data_sensitivity == 'personal_data':
            base_score += 3.0
        elif data_sensitivity == 'confidential':
            base_score += 2.0
        elif data_sensitivity == 'internal':
            base_score += 1.0

        # Cross-border data transfer risk
        regulatory_scope = system_context.get('regulatory_scope', [])
        if isinstance(regulatory_scope, list) and 'GDPR' in regulatory_scope:
            base_score += 1.0

        # System exposure and access
        users_affected = system_context.get('users_affected', 0)
        if users_affected > 1000000:
            base_score += 1.5
        elif users_affected > 100000:
            base_score += 1.0

        # Deployment environment risk
        deployment = system_context.get('deployment_status', '')
        if deployment == 'production':
            base_score += 0.5

        return min(10.0, max(1.0, base_score))

    def _calculate_explainability_risk(self, system_context: Dict[str, Any], ai_analysis: Dict[str, Any]) -> float:
        """Calculate explainability and transparency risk score"""
        base_score = 2.0

        # Model complexity inference from system type
        system_type = system_context.get('system_type', '')
        complex_types = ['computer_vision', 'natural_language_processing', 'medical_ai']
        if system_type in complex_types:
            base_score += 2.5
        elif system_type in ['recommendation_system', 'fraud_detection']:
            base_score += 1.5

        # Decision automation increases explainability requirements
        automation = system_context.get('decision_automation', '')
        if automation in ['high', 'full']:
            base_score += 2.0
        elif automation == 'medium':
            base_score += 1.0

        # High-impact decisions require more explainability
        business_impact = system_context.get('business_impact', '')
        if business_impact in ['critical', 'high']:
            base_score += 1.5

        # Regulatory requirements for explainability
        regulatory_scope = system_context.get('regulatory_scope', [])
        if isinstance(regulatory_scope, list):
            if 'EU_AI_Act' in regulatory_scope:
                base_score += 1.0
            if 'GDPR' in regulatory_scope:
                base_score += 0.5

        return min(10.0, max(1.0, base_score))

    def _calculate_regulatory_risk(self, system_context: Dict[str, Any], ai_analysis: Dict[str, Any]) -> float:
        """Calculate regulatory compliance risk score"""
        base_score = 2.0

        # Number of applicable regulations
        regulatory_scope = system_context.get('regulatory_scope', [])
        if isinstance(regulatory_scope, list):
            base_score += len(regulatory_scope) * 0.5

        # High-risk system types under EU AI Act
        system_type = system_context.get('system_type', '')
        high_risk_types = ['automated_decision_making', 'hiring_systems', 'medical_ai', 'credit_assessment']
        if system_type in high_risk_types:
            base_score += 3.0

        # Cross-jurisdictional complexity
        if isinstance(regulatory_scope, list) and len(regulatory_scope) > 3:
            base_score += 1.0

        # Business impact affects regulatory scrutiny
        business_impact = system_context.get('business_impact', '')
        if business_impact == 'critical':
            base_score += 1.5
        elif business_impact == 'high':
            base_score += 1.0

        return min(10.0, max(1.0, base_score))

    def _calculate_operational_risk(self, system_context: Dict[str, Any], ai_analysis: Dict[str, Any]) -> float:
        """Calculate operational risk score"""
        base_score = 2.0

        # Business criticality
        business_impact = system_context.get('business_impact', '')
        if business_impact == 'critical':
            base_score += 2.0
        elif business_impact == 'high':
            base_score += 1.0

        # Scale of operation
        users_affected = system_context.get('users_affected', 0)
        if users_affected > 1000000:
            base_score += 1.5
        elif users_affected > 100000:
            base_score += 1.0

        # Deployment maturity
        deployment = system_context.get('deployment_status', '')
        if deployment in ['development', 'testing']:
            base_score += 1.0
        elif deployment == 'staging':
            base_score += 0.5

        return min(10.0, max(1.0, base_score))

    def _calculate_overall_risk_score(self, dimensional_scores: Dict[str, Any]) -> float:
        """Calculate weighted overall risk score"""
        total_score = 0.0

        for dimension, data in dimensional_scores.items():
            score = data['score']
            weight = data['weight']
            total_score += score * weight

        return min(10.0, max(1.0, total_score))

    def _determine_risk_level(self, overall_risk: float) -> str:
        """Determine categorical risk level from numeric score"""
        if overall_risk >= self.risk_thresholds['critical']:
            return 'critical'
        elif overall_risk >= self.risk_thresholds['high']:
            return 'high'
        elif overall_risk >= self.risk_thresholds['medium']:
            return 'medium'
        else:
            return 'low'

    def _assess_regulatory_compliance(self, system_context: Dict[str, Any],
                                    dimensional_scores: Dict[str, Any]) -> Dict[str, Any]:
        """Assess compliance against applicable regulatory frameworks"""
        regulatory_scope = system_context.get('regulatory_scope', [])
        if not isinstance(regulatory_scope, list):
            regulatory_scope = []

        compliance_assessment = {}

        for framework in regulatory_scope:
            if framework == 'EU_AI_Act':
                compliance_assessment[framework] = self._assess_eu_ai_act_compliance(system_context, dimensional_scores)
            elif framework == 'GDPR':
                compliance_assessment[framework] = self._assess_gdpr_compliance(system_context, dimensional_scores)
            elif framework == 'NIST_AI_RMF':
                compliance_assessment[framework] = self._assess_nist_compliance(system_context, dimensional_scores)
            else:
                compliance_assessment[framework] = {
                    'status': 'requires_review',
                    'risk_level': 'medium',
                    'recommendations': [f'Conduct detailed {framework} compliance assessment']
                }

        return compliance_assessment

    def _generate_risk_mitigation_recommendations(self, dimensional_scores: Dict[str, Any],
                                                regulatory_assessment: Dict[str, Any],
                                                system_context: Dict[str, Any]) -> List[str]:
        """Generate prioritized risk mitigation recommendations"""
        recommendations = []

        # Bias mitigation recommendations
        bias_score = dimensional_scores.get('bias_fairness', {}).get('score', 0)
        if bias_score >= 6.0:
            recommendations.extend([
                'Implement comprehensive bias testing across protected characteristics',
                'Deploy algorithmic auditing tools for continuous bias monitoring',
                'Establish demographic parity and equalized odds constraints'
            ])

        # Privacy/Security recommendations
        privacy_score = dimensional_scores.get('privacy_security', {}).get('score', 0)
        if privacy_score >= 6.0:
            recommendations.extend([
                'Implement privacy-preserving techniques (differential privacy, federated learning)',
                'Enhance data encryption and access controls',
                'Conduct privacy impact assessment'
            ])

        # Explainability recommendations
        explainability_score = dimensional_scores.get('explainability', {}).get('score', 0)
        if explainability_score >= 6.0:
            recommendations.extend([
                'Implement explainable AI techniques (LIME, SHAP, attention mechanisms)',
                'Develop user-appropriate explanation interfaces',
                'Create model documentation and decision audit trails'
            ])

        # Regulatory compliance recommendations
        for framework, assessment in regulatory_assessment.items():
            if assessment.get('status') != 'compliant':
                recommendations.extend(assessment.get('recommendations', []))

        return recommendations[:10]  # Limit to top 10 recommendations

    def _generate_assessment_summary(self, overall_risk: float, risk_level: str,
                                   dimensional_scores: Dict[str, Any]) -> str:
        """Generate human-readable assessment summary"""
        highest_risk_dimension = max(dimensional_scores.items(),
                                   key=lambda x: x[1]['score'])

        summary = f"Overall risk level: {risk_level.upper()} (score: {overall_risk:.1f}/10). "
        summary += f"Primary risk area: {highest_risk_dimension[0].replace('_', ' ')} "
        summary += f"(score: {highest_risk_dimension[1]['score']:.1f}/10). "

        if overall_risk >= 7.0:
            summary += "Immediate governance review and mitigation required."
        elif overall_risk >= 4.0:
            summary += "Enhanced monitoring and risk controls recommended."
        else:
            summary += "Standard governance controls appear adequate."

        return summary

    # Risk factor extraction methods
    def _get_bias_risk_factors(self, system_context: Dict[str, Any], ai_analysis: Dict[str, Any]) -> List[str]:
        """Extract bias-specific risk factors"""
        factors = []

        if system_context.get('system_type') in ['automated_decision_making', 'hiring_systems']:
            factors.append('High-impact automated decisions affecting individuals')

        if system_context.get('decision_automation') in ['high', 'full']:
            factors.append('Limited human oversight of automated decisions')

        if system_context.get('users_affected', 0) > 100000:
            factors.append('Large-scale impact across diverse populations')

        return factors

    def _get_privacy_security_factors(self, system_context: Dict[str, Any], ai_analysis: Dict[str, Any]) -> List[str]:
        """Extract privacy and security risk factors"""
        factors = []

        data_sensitivity = system_context.get('data_sensitivity', '')
        if data_sensitivity in ['personal_data', 'sensitive_personal']:
            factors.append(f'Processing of {data_sensitivity.replace("_", " ")}')

        regulatory_scope = system_context.get('regulatory_scope', [])
        if isinstance(regulatory_scope, list) and 'GDPR' in regulatory_scope:
            factors.append('GDPR compliance requirements for data processing')

        return factors

    def _get_explainability_factors(self, system_context: Dict[str, Any], ai_analysis: Dict[str, Any]) -> List[str]:
        """Extract explainability risk factors"""
        factors = []

        if system_context.get('system_type') in ['computer_vision', 'natural_language_processing']:
            factors.append('Complex model architecture reducing interpretability')

        if system_context.get('decision_automation') in ['high', 'full']:
            factors.append('High automation requiring decision transparency')

        return factors

    def _get_regulatory_factors(self, system_context: Dict[str, Any], ai_analysis: Dict[str, Any]) -> List[str]:
        """Extract regulatory compliance risk factors"""
        factors = []

        regulatory_scope = system_context.get('regulatory_scope', [])
        if isinstance(regulatory_scope, list):
            if len(regulatory_scope) > 3:
                factors.append('Multiple overlapping regulatory requirements')

            if 'EU_AI_Act' in regulatory_scope:
                factors.append('EU AI Act high-risk system classification')

        return factors

    def _get_operational_factors(self, system_context: Dict[str, Any], ai_analysis: Dict[str, Any]) -> List[str]:
        """Extract operational risk factors"""
        factors = []

        if system_context.get('business_impact') in ['critical', 'high']:
            factors.append('High business impact from system failures')

        if system_context.get('deployment_status') in ['development', 'testing']:
            factors.append('Immature deployment status increasing operational risk')

        return factors
