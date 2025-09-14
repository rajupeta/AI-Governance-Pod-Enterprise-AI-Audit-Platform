#!/usr/bin/env python3
"""
Policy Compliance Agent for AI Governance System
Ensures AI systems comply with governance policies and regulatory frameworks
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import json
from .base_agent import BaseGovernanceAgent

logger = logging.getLogger(__name__)

class PolicyAgent(BaseGovernanceAgent):
    """
    Specialized agent for AI policy compliance checking
    Evaluates compliance with regulatory frameworks and internal policies
    """
    
    def __init__(self, knowledge_store, governance_db):
        """Initialize Policy Compliance Agent"""
        super().__init__(knowledge_store, governance_db, "policy_compliance")
        
        # Supported regulatory frameworks
        self.regulatory_frameworks = {
            'EU_AI_Act': {
                'name': 'European Union AI Act',
                'version': '2024',
                'risk_categories': ['prohibited', 'high_risk', 'limited_risk', 'minimal_risk'],
                'compliance_requirements': [
                    'risk_assessment', 'data_governance', 'transparency',
                    'human_oversight', 'accuracy_robustness', 'documentation'
                ]
            },
            'NIST_AI_RMF': {
                'name': 'NIST AI Risk Management Framework',
                'version': '1.0',
                'functions': ['govern', 'map', 'measure', 'manage'],
                'compliance_requirements': [
                    'ai_impact_assessment', 'risk_management_plan',
                    'continuous_monitoring', 'stakeholder_engagement'
                ]
            },
            'ISO_42001': {
                'name': 'ISO/IEC 42001:2023 AI Management System',
                'version': '2023',
                'requirements': [
                    'ai_policy', 'risk_management', 'competence_management',
                    'operational_planning', 'performance_evaluation'
                ]
            },
            'GDPR_AI': {
                'name': 'GDPR AI-Specific Requirements',
                'version': '2024',
                'requirements': [
                    'privacy_by_design', 'data_subject_rights',
                    'automated_decision_making', 'data_protection_impact_assessment'
                ]
            }
        }
    
    def check_policy_compliance(self, system_id: str, system_context: Dict, 
                              risk_factors: List[str]) -> Dict[str, Any]:
        """Comprehensive policy compliance assessment"""
        try:
            start_time = datetime.now()
            
            # Create policy compliance prompt
            compliance_prompt = self._create_compliance_prompt(
                system_context, risk_factors
            )
            
            # Generate AI-powered compliance analysis
            compliance_analysis = self._generate_governance_response(
                compliance_prompt, system_context
            )
            
            # Extract structured compliance data
            structured_compliance = self._extract_governance_data(
                compliance_analysis, "policy_compliance"
            )
            
            # Check compliance against each framework
            framework_compliance = self._check_framework_compliance(
                system_context, risk_factors
            )
            
            # Identify compliance gaps
            compliance_gaps = self._identify_compliance_gaps(
                framework_compliance, structured_compliance
            )
            
            # Generate remediation actions
            remediation_actions = self._generate_remediation_actions(
                compliance_gaps, framework_compliance
            )
            
            # Calculate overall compliance score
            compliance_score = self._calculate_compliance_score(framework_compliance)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Prepare comprehensive compliance result
            compliance_result = {
                'system_id': system_id,
                'assessment_id': self._create_assessment_id(),
                'status': self._determine_compliance_status(compliance_score),
                'compliance_score': compliance_score,
                'frameworks': framework_compliance,
                'gaps': compliance_gaps,
                'remediation_actions': remediation_actions,
                'regulatory_requirements': self._map_regulatory_requirements(
                    system_context, risk_factors
                ),
                'compliance_percentage': compliance_score,
                'next_review_date': self._calculate_next_review_date(compliance_score),
                'confidence_level': structured_compliance.get('confidence_level', 7),
                'processing_time': processing_time,
                'timestamp': datetime.now().isoformat()
            }
            
            # Log the compliance assessment interaction
            self._log_governance_interaction(
                system_id=system_id,
                interaction_type='policy_compliance',
                input_data={'context': system_context, 'risks': risk_factors},
                output_data=compliance_result,
                processing_time=processing_time
            )
            
            return compliance_result
            
        except Exception as e:
            logger.error(f"Failed to check policy compliance for {system_id}: {str(e)}")
            return self._get_fallback_compliance_result(system_id)
    
    def search_policy_knowledge(self, query: str, policy_type: str = 'all') -> List[Dict]:
        """Search governance policy knowledge base"""
        try:
            # Use ChromaDB to search policy documents
            search_results = self.knowledge_store.search_policies(query, policy_type)
            
            # Enhance results with AI analysis
            enhanced_results = []
            for result in search_results:
                enhanced_result = {
                    'policy_id': result.get('id'),
                    'title': result.get('title'),
                    'content': result.get('content'),
                    'policy_type': result.get('type', policy_type),
                    'regulatory_framework': result.get('framework'),
                    'relevance_score': result.get('score', 0),
                    'compliance_requirements': self._extract_compliance_requirements(
                        result.get('content', '')
                    ),
                    'applicability': self._assess_policy_applicability(
                        result, query
                    )
                }
                enhanced_results.append(enhanced_result)
            
            return enhanced_results[:10]  # Limit to top 10 results
            
        except Exception as e:
            logger.error(f"Failed to search policy knowledge: {str(e)}")
            return []
    
    def generate_policy_recommendations(self, system_id: str, 
                                      assessment_results: Dict) -> List[Dict]:
        """Generate specific policy recommendations based on assessment"""
        try:
            recommendations = []
            
            # Analyze compliance gaps
            gaps = assessment_results.get('gaps', [])
            compliance_score = assessment_results.get('compliance_score', 0)
            
            if compliance_score < 70:
                recommendations.append({
                    'priority': 'critical',
                    'category': 'compliance_improvement',
                    'title': 'Urgent Compliance Review Required',
                    'description': 'System compliance score is below acceptable threshold',
                    'actions': [
                        'Conduct comprehensive governance review',
                        'Engage legal and compliance teams',
                        'Develop compliance improvement plan',
                        'Consider deployment restrictions until compliant'
                    ],
                    'timeline': '2-4 weeks',
                    'regulatory_basis': 'Multiple framework requirements'
                })
            
            # Framework-specific recommendations
            for framework, status in assessment_results.get('frameworks', {}).items():
                if status.get('status') != 'compliant':
                    framework_info = self.regulatory_frameworks.get(framework, {})
                    recommendations.append({
                        'priority': 'high',
                        'category': 'framework_compliance',
                        'title': f'{framework_info.get("name", framework)} Compliance',
                        'description': f'Address {framework} compliance gaps',
                        'actions': status.get('requirements', []),
                        'timeline': '4-8 weeks',
                        'regulatory_basis': framework
                    })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate policy recommendations: {str(e)}")
            return []
    
    def _create_compliance_prompt(self, system_context: Dict, 
                                risk_factors: List[str]) -> str:
        """Create specialized prompt for compliance assessment"""
        specific_instructions = f"""
You are conducting a comprehensive AI system policy compliance assessment.

SYSTEM RISK FACTORS: {json.dumps(risk_factors)}

COMPLIANCE ASSESSMENT FRAMEWORK:
Evaluate compliance across these regulatory frameworks:

1. EU AI ACT COMPLIANCE:
   - Determine AI system risk category (prohibited/high/limited/minimal)
   - Check conformity assessment requirements
   - Verify CE marking obligations (if applicable)
   - Assess risk management system implementation
   - Review data governance and quality requirements
   - Evaluate transparency and information disclosure
   - Check human oversight and control measures

2. NIST AI RISK MANAGEMENT FRAMEWORK:
   - Assess AI impact and risk evaluation
   - Review governance and oversight structures
   - Evaluate risk management processes
   - Check continuous monitoring implementation
   - Assess stakeholder engagement practices

3. ISO 42001 AI MANAGEMENT SYSTEM:
   - Review AI policy documentation
   - Assess risk management procedures
   - Check competence and training programs
   - Evaluate operational planning and control
   - Review performance monitoring and evaluation

4. GDPR AI-SPECIFIC REQUIREMENTS:
   - Assess privacy by design implementation
   - Review automated decision-making compliance
   - Check data subject rights implementation
   - Evaluate data protection impact assessments

For each framework:
- Identify specific compliance requirements
- Assess current compliance status (compliant/partial/non-compliant)
- Identify gaps and deficiencies
- Provide specific remediation actions
- Estimate compliance timeline and effort

Focus on actionable compliance guidance and regulatory accuracy.
"""
        
        return self._create_governance_prompt(specific_instructions)
    
    def _check_framework_compliance(self, system_context: Dict, 
                                  risk_factors: List[str]) -> Dict[str, Dict]:
        """Check compliance against each regulatory framework"""
        compliance_results = {}
        
        for framework_id, framework_info in self.regulatory_frameworks.items():
            compliance_results[framework_id] = self._assess_framework_compliance(
                framework_id, framework_info, system_context, risk_factors
            )
        
        return compliance_results
    
    def _assess_framework_compliance(self, framework_id: str, framework_info: Dict,
                                   system_context: Dict, risk_factors: List[str]) -> Dict:
        """Assess compliance with a specific regulatory framework"""
        if framework_id == 'EU_AI_Act':
            return self._assess_eu_ai_act_compliance(system_context, risk_factors)
        elif framework_id == 'NIST_AI_RMF':
            return self._assess_nist_compliance(system_context, risk_factors)
        elif framework_id == 'ISO_42001':
            return self._assess_iso_compliance(system_context, risk_factors)
        elif framework_id == 'GDPR_AI':
            return self._assess_gdpr_ai_compliance(system_context, risk_factors)
        else:
            return self._get_default_framework_assessment(framework_id)
    
    def _assess_eu_ai_act_compliance(self, system_context: Dict, 
                                   risk_factors: List[str]) -> Dict:
        """Detailed EU AI Act compliance assessment"""
        # Determine risk category
        risk_category = self._determine_eu_ai_act_risk_category(
            system_context, risk_factors
        )
        
        compliance_requirements = []
        compliance_status = 'compliant'
        
        if risk_category == 'prohibited':
            compliance_status = 'non_compliant'
            compliance_requirements = ['System may be prohibited under EU AI Act']
        elif risk_category == 'high_risk':
            compliance_status = 'requires_assessment'
            compliance_requirements = [
                'Conformity assessment procedure required',
                'CE marking required',
                'Risk management system implementation',
                'Data governance measures',
                'Transparency and information disclosure',
                'Human oversight requirements',
                'Accuracy and robustness measures'
            ]
        elif risk_category == 'limited_risk':
            compliance_requirements = [
                'Transparency obligations',
                'Information disclosure to users'
            ]
        else:  # minimal_risk
            compliance_requirements = [
                'Basic transparency measures (recommended)'
            ]
        
        return {
            'status': compliance_status,
            'risk_category': risk_category,
            'requirements': compliance_requirements,
            'compliance_percentage': self._calculate_framework_compliance_percentage(
                compliance_status, risk_category
            ),
            'next_actions': self._get_eu_ai_act_next_actions(risk_category)
        }
    
    def _assess_nist_compliance(self, system_context: Dict, 
                              risk_factors: List[str]) -> Dict:
        """NIST AI RMF compliance assessment"""
        return {
            'status': 'partially_compliant',
            'requirements': [
                'AI impact assessment',
                'Risk management plan',
                'Continuous monitoring system',
                'Stakeholder engagement process'
            ],
            'compliance_percentage': 60,
            'next_actions': [
                'Complete AI impact assessment',
                'Implement continuous monitoring'
            ]
        }
    
    def _assess_iso_compliance(self, system_context: Dict, 
                             risk_factors: List[str]) -> Dict:
        """ISO 42001 compliance assessment"""
        return {
            'status': 'requires_review',
            'requirements': [
                'AI policy documentation',
                'Risk management procedures',
                'Competence management',
                'Performance evaluation system'
            ],
            'compliance_percentage': 40,
            'next_actions': [
                'Develop AI policy documentation',
                'Implement risk management procedures'
            ]
        }
    
    def _assess_gdpr_ai_compliance(self, system_context: Dict, 
                                 risk_factors: List[str]) -> Dict:
        """GDPR AI-specific compliance assessment"""
        return {
            'status': 'compliant',
            'requirements': [
                'Privacy by design implementation',
                'Data subject rights',
                'Automated decision-making transparency'
            ],
            'compliance_percentage': 85,
            'next_actions': [
                'Regular privacy compliance review'
            ]
        }
    
    def _determine_eu_ai_act_risk_category(self, system_context: Dict, 
                                         risk_factors: List[str]) -> str:
        """Determine EU AI Act risk category for the system"""
        # Check for prohibited AI practices
        prohibited_indicators = [
            'subliminal techniques', 'cognitive behavioral manipulation',
            'social scoring', 'real-time biometric identification'
        ]
        
        # Check for high-risk AI systems
        high_risk_indicators = [
            'biometric identification', 'critical infrastructure',
            'education access', 'employment decisions', 'credit scoring',
            'law enforcement', 'migration asylum', 'administration of justice'
        ]
        
        context_text = json.dumps(system_context).lower()
        risk_text = ' '.join(risk_factors).lower()
        all_text = context_text + ' ' + risk_text
        
        if any(indicator in all_text for indicator in prohibited_indicators):
            return 'prohibited'
        elif any(indicator in all_text for indicator in high_risk_indicators):
            return 'high_risk'
        elif 'chatbot' in all_text or 'deepfake' in all_text:
            return 'limited_risk'
        else:
            return 'minimal_risk'
    
    def _identify_compliance_gaps(self, framework_compliance: Dict, 
                                structured_compliance: Dict) -> List[Dict]:
        """Identify specific compliance gaps"""
        gaps = []
        
        for framework, status in framework_compliance.items():
            if status.get('status') != 'compliant':
                gap = {
                    'framework': framework,
                    'gap_type': 'framework_compliance',
                    'severity': self._assess_gap_severity(status.get('status')),
                    'description': f'{framework} compliance requirements not met',
                    'requirements': status.get('requirements', []),
                    'estimated_effort': self._estimate_compliance_effort(status),
                    'priority': 'high' if status.get('status') == 'non_compliant' else 'medium'
                }
                gaps.append(gap)
        
        return gaps
    
    def _generate_remediation_actions(self, compliance_gaps: List[Dict], 
                                    framework_compliance: Dict) -> List[Dict]:
        """Generate specific remediation actions for compliance gaps"""
        actions = []
        
        for gap in compliance_gaps:
            if gap['framework'] == 'EU_AI_Act':
                actions.extend(self._generate_eu_ai_act_actions(gap))
            elif gap['framework'] == 'NIST_AI_RMF':
                actions.extend(self._generate_nist_actions(gap))
            elif gap['framework'] == 'ISO_42001':
                actions.extend(self._generate_iso_actions(gap))
            elif gap['framework'] == 'GDPR_AI':
                actions.extend(self._generate_gdpr_actions(gap))
        
        return actions
    
    def _generate_eu_ai_act_actions(self, gap: Dict) -> List[Dict]:
        """Generate EU AI Act specific remediation actions"""
        return [{
            'action': 'Conduct EU AI Act conformity assessment',
            'priority': 'critical',
            'timeline': '8-12 weeks',
            'description': 'Complete formal conformity assessment procedure',
            'responsible_party': 'Legal and Compliance Team',
            'regulatory_basis': 'EU AI Act Article 43'
        }]
    
    def _generate_nist_actions(self, gap: Dict) -> List[Dict]:
        """Generate NIST AI RMF specific remediation actions"""
        return [{
            'action': 'Implement NIST AI RMF governance framework',
            'priority': 'high',
            'timeline': '6-8 weeks',
            'description': 'Establish AI risk management processes per NIST guidelines',
            'responsible_party': 'AI Governance Team',
            'regulatory_basis': 'NIST AI RMF 1.0'
        }]
    
    def _generate_iso_actions(self, gap: Dict) -> List[Dict]:
        """Generate ISO 42001 specific remediation actions"""
        return [{
            'action': 'Develop ISO 42001 AI management system',
            'priority': 'medium',
            'timeline': '10-12 weeks',
            'description': 'Implement AI management system per ISO 42001 requirements',
            'responsible_party': 'Quality Management Team',
            'regulatory_basis': 'ISO/IEC 42001:2023'
        }]
    
    def _generate_gdpr_actions(self, gap: Dict) -> List[Dict]:
        """Generate GDPR AI specific remediation actions"""
        return [{
            'action': 'Enhance GDPR AI compliance measures',
            'priority': 'medium',
            'timeline': '4-6 weeks',
            'description': 'Strengthen privacy by design and data subject rights',
            'responsible_party': 'Data Protection Officer',
            'regulatory_basis': 'GDPR Articles 22, 25'
        }]
    
    def _calculate_compliance_score(self, framework_compliance: Dict) -> float:
        """Calculate overall compliance score"""
        total_score = 0
        framework_count = len(framework_compliance)
        
        for framework_result in framework_compliance.values():
            total_score += framework_result.get('compliance_percentage', 0)
        
        return round(total_score / framework_count, 1) if framework_count > 0 else 0
    
    def _determine_compliance_status(self, compliance_score: float) -> str:
        """Determine overall compliance status"""
        if compliance_score >= 90:
            return 'fully_compliant'
        elif compliance_score >= 70:
            return 'mostly_compliant'
        elif compliance_score >= 50:
            return 'partially_compliant'
        else:
            return 'non_compliant'
    
    def _calculate_next_review_date(self, compliance_score: float) -> str:
        """Calculate when next compliance review should occur"""
        if compliance_score < 50:
            months = 1  # Monthly review for non-compliant systems
        elif compliance_score < 70:
            months = 3  # Quarterly review for partial compliance
        elif compliance_score < 90:
            months = 6  # Semi-annual review for mostly compliant
        else:
            months = 12  # Annual review for fully compliant
        
        review_date = datetime.now()
        # Add months (simplified - doesn't handle month boundaries perfectly)
        review_date = review_date.replace(
            month=review_date.month + months if review_date.month + months <= 12
            else (review_date.month + months - 12),
            year=review_date.year + (1 if review_date.month + months > 12 else 0)
        )
        
        return review_date.strftime('%Y-%m-%d')
    
    def _map_regulatory_requirements(self, system_context: Dict, 
                                   risk_factors: List[str]) -> Dict[str, List]:
        """Map applicable regulatory requirements"""
        requirements = {
            'mandatory': [],
            'recommended': [],
            'conditional': []
        }
        
        # EU AI Act requirements
        if self._determine_eu_ai_act_risk_category(system_context, risk_factors) == 'high_risk':
            requirements['mandatory'].extend([
                'EU AI Act conformity assessment',
                'CE marking',
                'Risk management system'
            ])
        
        # NIST requirements (typically recommended for US systems)
        requirements['recommended'].extend([
            'AI impact assessment',
            'Continuous monitoring'
        ])
        
        return requirements
    
    def _assess_gap_severity(self, status: str) -> str:
        """Assess the severity of a compliance gap"""
        if status == 'non_compliant':
            return 'critical'
        elif status == 'requires_assessment':
            return 'high'
        elif status == 'partially_compliant':
            return 'medium'
        else:
            return 'low'
    
    def _estimate_compliance_effort(self, status: Dict) -> str:
        """Estimate effort required to achieve compliance"""
        compliance_percentage = status.get('compliance_percentage', 0)
        
        if compliance_percentage < 30:
            return 'high (12+ weeks)'
        elif compliance_percentage < 60:
            return 'medium (6-12 weeks)'
        elif compliance_percentage < 80:
            return 'low (2-6 weeks)'
        else:
            return 'minimal (1-2 weeks)'
    
    def _calculate_framework_compliance_percentage(self, status: str, 
                                                 risk_category: str) -> float:
        """Calculate compliance percentage for a framework"""
        if status == 'compliant':
            return 100.0
        elif status == 'partially_compliant':
            return 60.0
        elif status == 'requires_assessment':
            return 30.0 if risk_category == 'high_risk' else 70.0
        else:  # non_compliant
            return 0.0
    
    def _get_eu_ai_act_next_actions(self, risk_category: str) -> List[str]:
        """Get next actions for EU AI Act compliance"""
        if risk_category == 'prohibited':
            return ['Discontinue system or modify to remove prohibited practices']
        elif risk_category == 'high_risk':
            return ['Initiate conformity assessment procedure', 'Engage notified body']
        elif risk_category == 'limited_risk':
            return ['Implement transparency measures', 'Update user disclosures']
        else:
            return ['Monitor regulatory developments', 'Maintain documentation']
    
    def _extract_compliance_requirements(self, content: str) -> List[str]:
        """Extract compliance requirements from policy content"""
        # This would use NLP to extract requirements
        # For now, return basic requirements
        return [
            'Documentation required',
            'Regular review needed',
            'Stakeholder notification'
        ]
    
    def _assess_policy_applicability(self, policy_result: Dict, query: str) -> str:
        """Assess how applicable a policy is to the query"""
        score = policy_result.get('score', 0)
        
        if score > 0.8:
            return 'highly_applicable'
        elif score > 0.6:
            return 'applicable'
        elif score > 0.4:
            return 'somewhat_applicable'
        else:
            return 'low_applicability'
    
    def _get_default_framework_assessment(self, framework_id: str) -> Dict:
        """Default assessment for unknown frameworks"""
        return {
            'status': 'unknown',
            'requirements': ['Framework assessment not implemented'],
            'compliance_percentage': 0,
            'next_actions': ['Manual review required']
        }
    
    def _get_fallback_compliance_result(self, system_id: str) -> Dict[str, Any]:
        """Provide fallback compliance result when processing fails"""
        return {
            'system_id': system_id,
            'assessment_id': self._create_assessment_id(),
            'status': 'assessment_failed',
            'compliance_score': 0,
            'frameworks': {},
            'gaps': [{'description': 'Policy compliance assessment failed'}],
            'remediation_actions': [{
                'action': 'Manual policy review required',
                'priority': 'high',
                'description': 'Automated compliance assessment failed'
            }],
            'error': 'Policy compliance assessment failed',
            'timestamp': datetime.now().isoformat()
        }