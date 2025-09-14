#!/usr/bin/env python3
"""
Bias Detection Agent for AI Governance System
Detects and analyzes bias in AI systems with fairness evaluation
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import json
from .base_agent import BaseGovernanceAgent

logger = logging.getLogger(__name__)

class BiasAgent(BaseGovernanceAgent):
    """
    Specialized agent for AI system bias detection and analysis
    Evaluates fairness across protected groups and identifies bias patterns
    """
    
    def __init__(self, knowledge_store, governance_db):
        """Initialize Bias Detection Agent"""
        super().__init__(knowledge_store, governance_db, "bias_detection")
        
        # Protected attributes for bias analysis
        self.protected_attributes = {
            'demographic': [
                'race', 'ethnicity', 'gender', 'age', 'religion',
                'sexual_orientation', 'nationality', 'disability_status'
            ],
            'socioeconomic': [
                'income_level', 'education_level', 'employment_status',
                'geographic_location', 'social_class'
            ],
            'behavioral': [
                'credit_history', 'online_behavior', 'purchase_history',
                'social_media_activity'
            ]
        }
        
        # Fairness metrics for evaluation
        self.fairness_metrics = {
            'individual_fairness': 'Similar individuals should receive similar outcomes',
            'group_fairness': 'Outcomes should be similar across protected groups',
            'demographic_parity': 'Equal positive prediction rates across groups',
            'equalized_odds': 'Equal true positive and false positive rates',
            'calibration': 'Prediction probabilities should be well-calibrated',
            'counterfactual_fairness': 'Decisions should be the same in counterfactual world'
        }
    
    def analyze_system_bias(self, system_id: str, system_context: Dict,
                          risk_assessment: Dict) -> Dict[str, Any]:
        """Comprehensive AI system bias analysis"""
        try:
            start_time = datetime.now()
            
            # Create bias analysis prompt
            bias_prompt = self._create_bias_analysis_prompt(
                system_context, risk_assessment
            )
            
            # Generate AI-powered bias analysis
            bias_analysis = self._generate_governance_response(
                bias_prompt, system_context
            )
            
            # Extract structured bias data
            structured_bias = self._extract_governance_data(
                bias_analysis, "bias_analysis"
            )
            
            # Perform detailed bias evaluation
            bias_evaluation = self._evaluate_bias_dimensions(
                structured_bias, system_context
            )
            
            # Assess fairness across protected groups
            fairness_assessment = self._assess_fairness_metrics(
                system_context, bias_evaluation
            )
            
            # Calculate bias risk scores
            bias_scores = self._calculate_bias_risk_scores(
                bias_evaluation, fairness_assessment
            )
            
            # Generate mitigation strategies
            mitigation_strategies = self._generate_bias_mitigation_strategies(
                bias_evaluation, bias_scores
            )
            
            # Check for algorithmic discrimination
            discrimination_analysis = self._analyze_algorithmic_discrimination(
                system_context, bias_evaluation
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Prepare comprehensive bias analysis result
            analysis_result = {
                'system_id': system_id,
                'assessment_id': self._create_assessment_id(),
                'bias_level': bias_scores['overall_bias_level'],
                'bias_risk_score': bias_scores['overall_bias_score'],
                'fairness_metrics': fairness_assessment,
                'bias_dimensions': {
                    'demographic_bias': bias_evaluation['demographic'],
                    'socioeconomic_bias': bias_evaluation['socioeconomic'],
                    'behavioral_bias': bias_evaluation['behavioral'],
                    'systemic_bias': bias_evaluation['systemic']
                },
                'discrimination_risks': discrimination_analysis,
                'protected_groups_impact': self._assess_protected_groups_impact(
                    system_context, bias_evaluation
                ),
                'mitigation_strategies': mitigation_strategies,
                'continuous_monitoring_plan': self._create_monitoring_plan(
                    bias_scores, system_context
                ),
                'confidence_level': structured_bias.get('confidence_level', 7),
                'processing_time': processing_time,
                'timestamp': datetime.now().isoformat()
            }
            
            # Log the bias analysis interaction
            self._log_governance_interaction(
                system_id=system_id,
                interaction_type='bias_analysis',
                input_data={'context': system_context, 'risk_assessment': risk_assessment},
                output_data=analysis_result,
                processing_time=processing_time
            )
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Failed to analyze bias for system {system_id}: {str(e)}")
            return self._get_fallback_bias_analysis(system_id)
    
    def monitor_bias_drift(self, system_id: str, monitoring_parameters: Dict) -> Dict[str, Any]:
        """Monitor for bias drift in deployed AI systems"""
        try:
            # Get historical bias assessments
            historical_data = self.governance_db.get_bias_history(system_id)
            
            # Analyze current bias indicators
            current_indicators = self._analyze_current_bias_indicators(
                system_id, monitoring_parameters
            )
            
            # Detect bias drift patterns
            drift_analysis = self._detect_bias_drift_patterns(
                historical_data, current_indicators
            )
            
            # Assess drift severity
            drift_severity = self._assess_drift_severity(drift_analysis)
            
            # Generate drift alerts if needed
            alerts = self._generate_bias_drift_alerts(
                drift_analysis, drift_severity
            )
            
            monitoring_result = {
                'system_id': system_id,
                'monitoring_timestamp': datetime.now().isoformat(),
                'bias_indicators': current_indicators,
                'drift_analysis': drift_analysis,
                'drift_severity': drift_severity,
                'alerts': alerts,
                'recommended_actions': self._generate_drift_response_actions(
                    drift_analysis, drift_severity
                ),
                'next_monitoring_date': self._calculate_next_monitoring_date(
                    drift_severity
                )
            }
            
            return monitoring_result
            
        except Exception as e:
            logger.error(f"Failed to monitor bias drift for system {system_id}: {str(e)}")
            return {'error': f'Bias drift monitoring failed: {str(e)}'}
    
    def _create_bias_analysis_prompt(self, system_context: Dict, 
                                   risk_assessment: Dict) -> str:
        """Create specialized prompt for bias analysis"""
        specific_instructions = f"""
You are conducting a comprehensive AI system bias and fairness analysis.

RISK ASSESSMENT CONTEXT: {json.dumps(risk_assessment.get('identified_risks', []))}

BIAS ANALYSIS FRAMEWORK:
Analyze the AI system for bias and fairness issues across these dimensions:

1. DEMOGRAPHIC BIAS:
   - Race, ethnicity, and nationality bias
   - Gender and gender identity discrimination
   - Age-based discrimination patterns
   - Religious and cultural bias
   - Disability and accessibility discrimination
   - Sexual orientation bias

2. SOCIOECONOMIC BIAS:
   - Income and wealth-based discrimination
   - Educational background bias
   - Employment status discrimination
   - Geographic and regional bias
   - Social class and status discrimination

3. BEHAVIORAL BIAS:
   - Historical behavior pattern discrimination
   - Credit and financial history bias
   - Online behavior and digital footprint bias
   - Purchase and consumption pattern bias
   - Social media activity discrimination

4. SYSTEMIC BIAS:
   - Institutional and structural bias propagation
   - Historical discrimination perpetuation
   - Proxy variable discrimination
   - Intersectional bias (multiple protected attributes)
   - Feedback loops and bias amplification

FAIRNESS METRICS EVALUATION:
For each bias dimension, assess:
- Individual fairness: Similar treatment for similar individuals
- Group fairness: Equal outcomes across protected groups
- Demographic parity: Equal positive rates across groups
- Equalized odds: Equal error rates across groups
- Calibration: Well-calibrated probability predictions
- Counterfactual fairness: Same decisions in alternative scenarios

ANALYSIS REQUIREMENTS:
- Identify specific bias risks and their likelihood
- Assess potential impact on protected groups
- Evaluate fairness metric violations
- Consider intersectional and compound bias effects
- Provide evidence-based bias severity ratings
- Suggest concrete mitigation strategies
- Consider legal and regulatory implications

Focus on actionable bias detection and practical mitigation approaches.
"""
        
        return self._create_governance_prompt(specific_instructions)
    
    def _evaluate_bias_dimensions(self, structured_bias: Dict, 
                                system_context: Dict) -> Dict[str, List]:
        """Evaluate bias across different dimensions"""
        bias_evaluation = {
            'demographic': [],
            'socioeconomic': [],
            'behavioral': [],
            'systemic': []
        }
        
        # Categorize identified bias risks
        for risk in structured_bias.get('risk_factors', []):
            risk_lower = risk.lower()
            
            # Demographic bias indicators
            if any(term in risk_lower for term in [
                'race', 'gender', 'age', 'religion', 'ethnicity', 'nationality', 'disability'
            ]):
                bias_evaluation['demographic'].append(risk)
            
            # Socioeconomic bias indicators
            elif any(term in risk_lower for term in [
                'income', 'education', 'employment', 'geographic', 'social class'
            ]):
                bias_evaluation['socioeconomic'].append(risk)
            
            # Behavioral bias indicators
            elif any(term in risk_lower for term in [
                'behavior', 'history', 'credit', 'purchase', 'online', 'social media'
            ]):
                bias_evaluation['behavioral'].append(risk)
            
            # Systemic bias indicators
            elif any(term in risk_lower for term in [
                'systemic', 'institutional', 'structural', 'feedback', 'proxy'
            ]):
                bias_evaluation['systemic'].append(risk)
            
            # Default to demographic if unclear
            else:
                bias_evaluation['demographic'].append(risk)
        
        return bias_evaluation
    
    def _assess_fairness_metrics(self, system_context: Dict, 
                               bias_evaluation: Dict) -> Dict[str, Any]:
        """Assess system against fairness metrics"""
        fairness_assessment = {}
        
        for metric, description in self.fairness_metrics.items():
            assessment = self._evaluate_fairness_metric(
                metric, system_context, bias_evaluation
            )
            fairness_assessment[metric] = {
                'description': description,
                'status': assessment['status'],
                'score': assessment['score'],
                'concerns': assessment.get('concerns', []),
                'recommendations': assessment.get('recommendations', [])
            }
        
        return fairness_assessment
    
    def _evaluate_fairness_metric(self, metric: str, system_context: Dict,
                                bias_evaluation: Dict) -> Dict:
        """Evaluate a specific fairness metric"""
        # Simplified fairness metric evaluation
        # In production, this would use actual model performance data
        
        total_bias_indicators = sum(len(risks) for risks in bias_evaluation.values())
        
        if metric == 'demographic_parity':
            if bias_evaluation['demographic']:
                return {
                    'status': 'concern',
                    'score': 4,
                    'concerns': ['Demographic bias indicators detected'],
                    'recommendations': ['Test equal positive rates across demographic groups']
                }
        elif metric == 'individual_fairness':
            if total_bias_indicators > 5:
                return {
                    'status': 'concern',
                    'score': 3,
                    'concerns': ['Multiple bias indicators suggest individual fairness issues'],
                    'recommendations': ['Implement individual fairness testing']
                }
        
        # Default assessment for other metrics
        return {
            'status': 'acceptable' if total_bias_indicators < 3 else 'concern',
            'score': max(1, 8 - total_bias_indicators),
            'concerns': [] if total_bias_indicators < 3 else ['Potential fairness concerns'],
            'recommendations': ['Regular fairness monitoring recommended']
        }
    
    def _calculate_bias_risk_scores(self, bias_evaluation: Dict, 
                                  fairness_assessment: Dict) -> Dict[str, Any]:
        """Calculate bias risk scores across dimensions"""
        dimension_scores = {}
        
        # Score each bias dimension
        for dimension, risks in bias_evaluation.items():
            base_score = len(risks) * 1.5  # Base score from risk count
            severity_multiplier = 2.0 if dimension == 'demographic' else 1.5
            dimension_scores[dimension] = min(10, base_score * severity_multiplier)
        
        # Factor in fairness metric concerns
        fairness_concerns = sum(1 for metric in fairness_assessment.values() 
                              if metric['status'] == 'concern')
        fairness_penalty = fairness_concerns * 0.5
        
        # Calculate overall bias score
        overall_score = (sum(dimension_scores.values()) / len(dimension_scores)) + fairness_penalty
        overall_score = min(10, overall_score)
        
        # Determine bias level
        if overall_score >= 8:
            bias_level = 'critical'
        elif overall_score >= 6:
            bias_level = 'high'
        elif overall_score >= 4:
            bias_level = 'medium'
        else:
            bias_level = 'low'
        
        return {
            'overall_bias_score': round(overall_score, 1),
            'overall_bias_level': bias_level,
            'dimension_scores': dimension_scores,
            'fairness_penalty': fairness_penalty
        }
    
    def _generate_bias_mitigation_strategies(self, bias_evaluation: Dict, 
                                           bias_scores: Dict) -> List[Dict]:
        """Generate specific bias mitigation strategies"""
        strategies = []
        
        # Demographic bias mitigation
        if bias_evaluation['demographic']:
            strategies.append({
                'category': 'demographic_bias',
                'priority': 'critical',
                'strategy': 'Implement demographic bias testing and mitigation',
                'techniques': [
                    'Fairness-aware machine learning algorithms',
                    'Demographic parity testing across protected groups',
                    'Adversarial debiasing during model training',
                    'Regular bias audits with diverse evaluation teams',
                    'Inclusive dataset collection and curation'
                ],
                'timeline': '4-8 weeks',
                'success_metrics': [
                    'Equal positive prediction rates across demographics',
                    'Reduced disparate impact ratios',
                    'Improved fairness metric scores'
                ]
            })
        
        # Socioeconomic bias mitigation
        if bias_evaluation['socioeconomic']:
            strategies.append({
                'category': 'socioeconomic_bias',
                'priority': 'high',
                'strategy': 'Address socioeconomic discrimination patterns',
                'techniques': [
                    'Socioeconomic proxy variable identification and removal',
                    'Income-blind algorithm design where appropriate',
                    'Geographic bias testing and correction',
                    'Educational access consideration in model design'
                ],
                'timeline': '6-10 weeks',
                'success_metrics': [
                    'Reduced correlation with socioeconomic indicators',
                    'Equal access across income levels',
                    'Geographic parity in outcomes'
                ]
            })
        
        # Behavioral bias mitigation
        if bias_evaluation['behavioral']:
            strategies.append({
                'category': 'behavioral_bias',
                'priority': 'medium',
                'strategy': 'Mitigate behavioral pattern discrimination',
                'techniques': [
                    'Historical bias correction in behavioral data',
                    'Temporal bias adjustment for changing behaviors',
                    'Context-aware behavioral interpretation',
                    'Privacy-preserving behavioral analysis'
                ],
                'timeline': '4-6 weeks',
                'success_metrics': [
                    'Reduced historical bias propagation',
                    'Fair treatment of behavioral changes',
                    'Privacy-compliant behavioral analysis'
                ]
            })
        
        # Systemic bias mitigation
        if bias_evaluation['systemic']:
            strategies.append({
                'category': 'systemic_bias',
                'priority': 'critical',
                'strategy': 'Address systemic and institutional bias',
                'techniques': [
                    'Intersectional bias analysis and mitigation',
                    'Feedback loop identification and interruption',
                    'Proxy discrimination detection and removal',
                    'Institutional bias awareness training',
                    'Regular bias impact assessments'
                ],
                'timeline': '8-12 weeks',
                'success_metrics': [
                    'Reduced intersectional discrimination',
                    'Eliminated harmful feedback loops',
                    'Comprehensive bias documentation'
                ]
            })
        
        return strategies
    
    def _analyze_algorithmic_discrimination(self, system_context: Dict, 
                                         bias_evaluation: Dict) -> Dict[str, Any]:
        """Analyze potential algorithmic discrimination"""
        discrimination_risks = {
            'direct_discrimination': self._assess_direct_discrimination(
                system_context, bias_evaluation
            ),
            'indirect_discrimination': self._assess_indirect_discrimination(
                system_context, bias_evaluation
            ),
            'intersectional_discrimination': self._assess_intersectional_discrimination(
                system_context, bias_evaluation
            )
        }
        
        overall_risk = self._calculate_discrimination_risk(discrimination_risks)
        
        return {
            'overall_risk': overall_risk,
            'discrimination_types': discrimination_risks,
            'legal_implications': self._assess_legal_implications(
                discrimination_risks, overall_risk
            ),
            'regulatory_requirements': self._map_anti_discrimination_requirements()
        }
    
    def _assess_protected_groups_impact(self, system_context: Dict, 
                                      bias_evaluation: Dict) -> Dict[str, Any]:
        """Assess impact on protected groups"""
        protected_groups_analysis = {}
        
        for category, attributes in self.protected_attributes.items():
            impact_assessment = {
                'category': category,
                'potential_impacts': [],
                'severity': 'low',
                'affected_groups': []
            }
            
            # Check for relevant bias indicators
            category_bias = bias_evaluation.get(category, [])
            if category_bias:
                impact_assessment['potential_impacts'] = category_bias
                impact_assessment['severity'] = 'high' if len(category_bias) > 2 else 'medium'
                impact_assessment['affected_groups'] = self._identify_affected_groups(
                    category, category_bias
                )
            
            protected_groups_analysis[category] = impact_assessment
        
        return protected_groups_analysis
    
    def _create_monitoring_plan(self, bias_scores: Dict, system_context: Dict) -> Dict[str, Any]:
        """Create continuous bias monitoring plan"""
        bias_level = bias_scores['overall_bias_level']
        
        if bias_level in ['critical', 'high']:
            monitoring_frequency = 'monthly'
            monitoring_depth = 'comprehensive'
        elif bias_level == 'medium':
            monitoring_frequency = 'quarterly'
            monitoring_depth = 'standard'
        else:
            monitoring_frequency = 'annually'
            monitoring_depth = 'basic'
        
        return {
            'monitoring_frequency': monitoring_frequency,
            'monitoring_depth': monitoring_depth,
            'key_metrics': [
                'Demographic parity ratios',
                'Equalized odds metrics',
                'Individual fairness scores'
            ],
            'alert_thresholds': {
                'bias_score_increase': 1.0,
                'fairness_metric_degradation': 0.1,
                'protected_group_impact_increase': 0.15
            },
            'stakeholder_reporting': {
                'frequency': monitoring_frequency,
                'recipients': ['AI Ethics Team', 'Legal Compliance', 'Product Management'],
                'report_format': 'bias_monitoring_dashboard'
            }
        }
    
    def _analyze_current_bias_indicators(self, system_id: str, 
                                       monitoring_parameters: Dict) -> Dict[str, Any]:
        """Analyze current bias indicators for monitoring"""
        return {
            'demographic_indicators': self._get_demographic_indicators(system_id),
            'fairness_metrics': self._get_current_fairness_metrics(system_id),
            'performance_disparities': self._get_performance_disparities(system_id),
            'feedback_patterns': self._analyze_feedback_patterns(system_id)
        }
    
    def _detect_bias_drift_patterns(self, historical_data: List[Dict], 
                                  current_indicators: Dict) -> Dict[str, Any]:
        """Detect patterns of bias drift over time"""
        if not historical_data:
            return {'drift_detected': False, 'reason': 'insufficient_historical_data'}
        
        # Simplified drift detection
        return {
            'drift_detected': False,
            'drift_direction': 'stable',
            'drift_magnitude': 0.0,
            'affected_metrics': [],
            'trend_analysis': 'stable'
        }
    
    def _assess_drift_severity(self, drift_analysis: Dict) -> str:
        """Assess severity of detected bias drift"""
        if not drift_analysis.get('drift_detected'):
            return 'none'
        
        magnitude = drift_analysis.get('drift_magnitude', 0)
        if magnitude > 0.3:
            return 'severe'
        elif magnitude > 0.1:
            return 'moderate'
        else:
            return 'minor'
    
    def _generate_bias_drift_alerts(self, drift_analysis: Dict, 
                                  drift_severity: str) -> List[Dict]:
        """Generate alerts for bias drift"""
        alerts = []
        
        if drift_severity in ['severe', 'moderate']:
            alerts.append({
                'type': 'bias_drift',
                'severity': drift_severity,
                'message': f'{drift_severity.title()} bias drift detected',
                'recommended_action': 'Immediate bias assessment and mitigation required',
                'priority': 'high' if drift_severity == 'severe' else 'medium'
            })
        
        return alerts
    
    def _generate_drift_response_actions(self, drift_analysis: Dict, 
                                       drift_severity: str) -> List[str]:
        """Generate recommended actions for bias drift"""
        if drift_severity == 'none':
            return ['Continue regular monitoring']
        elif drift_severity == 'minor':
            return ['Increase monitoring frequency', 'Review recent model changes']
        elif drift_severity == 'moderate':
            return ['Conduct bias assessment', 'Implement corrective measures', 'Notify stakeholders']
        else:  # severe
            return [
                'Immediate system review required',
                'Consider temporary system restrictions',
                'Emergency bias mitigation procedures',
                'Legal and compliance consultation'
            ]
    
    def _calculate_next_monitoring_date(self, drift_severity: str) -> str:
        """Calculate when next bias monitoring should occur"""
        if drift_severity in ['severe', 'moderate']:
            weeks = 2
        elif drift_severity == 'minor':
            weeks = 4
        else:
            weeks = 12
        
        next_date = datetime.now()
        import calendar
        next_date = next_date.replace(
            day=min(next_date.day + (weeks * 7), calendar.monthrange(next_date.year, next_date.month)[1])
        )
        
        return next_date.strftime('%Y-%m-%d')
    
    # Helper methods for detailed analysis
    def _assess_direct_discrimination(self, system_context: Dict, bias_evaluation: Dict) -> Dict:
        return {'risk_level': 'medium', 'indicators': bias_evaluation.get('demographic', [])}
    
    def _assess_indirect_discrimination(self, system_context: Dict, bias_evaluation: Dict) -> Dict:
        return {'risk_level': 'medium', 'indicators': bias_evaluation.get('systemic', [])}
    
    def _assess_intersectional_discrimination(self, system_context: Dict, bias_evaluation: Dict) -> Dict:
        return {'risk_level': 'low', 'indicators': []}
    
    def _calculate_discrimination_risk(self, discrimination_risks: Dict) -> str:
        risk_levels = [risk['risk_level'] for risk in discrimination_risks.values()]
        if 'high' in risk_levels:
            return 'high'
        elif 'medium' in risk_levels:
            return 'medium'
        else:
            return 'low'
    
    def _assess_legal_implications(self, discrimination_risks: Dict, overall_risk: str) -> List[str]:
        implications = []
        if overall_risk in ['high', 'medium']:
            implications.extend([
                'Potential civil rights violations',
                'Employment discrimination concerns',
                'Fair lending compliance issues'
            ])
        return implications
    
    def _map_anti_discrimination_requirements(self) -> List[str]:
        return [
            'Equal Employment Opportunity compliance',
            'Fair Credit Reporting Act requirements',
            'Americans with Disabilities Act compliance',
            'Civil Rights Act adherence'
        ]
    
    def _identify_affected_groups(self, category: str, bias_indicators: List[str]) -> List[str]:
        # Simplified group identification
        return ['Demographic groups', 'Protected classes']
    
    def _get_demographic_indicators(self, system_id: str) -> Dict:
        return {'indicators': [], 'status': 'monitoring'}
    
    def _get_current_fairness_metrics(self, system_id: str) -> Dict:
        return {'metrics': {}, 'status': 'monitoring'}
    
    def _get_performance_disparities(self, system_id: str) -> Dict:
        return {'disparities': [], 'status': 'monitoring'}
    
    def _analyze_feedback_patterns(self, system_id: str) -> Dict:
        return {'patterns': [], 'status': 'monitoring'}
    
    def _get_fallback_bias_analysis(self, system_id: str) -> Dict[str, Any]:
        """Provide fallback bias analysis when processing fails"""
        return {
            'system_id': system_id,
            'assessment_id': self._create_assessment_id(),
            'bias_level': 'unknown',
            'bias_risk_score': 5,
            'fairness_metrics': {},
            'mitigation_strategies': [{
                'category': 'system',
                'priority': 'high',
                'strategy': 'Manual bias assessment required',
                'techniques': ['Contact AI ethics team for manual review']
            }],
            'error': 'Automated bias analysis failed',
            'timestamp': datetime.now().isoformat()
        }