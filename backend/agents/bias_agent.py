#!/usr/bin/env python3
"""
Bias Detection Agent for AI Governance
Detects and analyzes bias in AI systems across protected characteristics
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from .base_agent import BaseGovernanceAgent

logger = logging.getLogger(__name__)

class BiasDetectionAgent(BaseGovernanceAgent):
    """
    Detects and analyzes bias in AI systems across protected characteristics
    - Statistical bias analysis across protected groups
    - Fairness metric calculation and monitoring
    - Bias mitigation strategy recommendations
    - Continuous bias monitoring and alerting
    """

    def __init__(self, knowledge_store, governance_db):
        """Initialize bias detection agent"""
        super().__init__(knowledge_store, governance_db, "bias_detection")

        # Protected characteristics for bias analysis
        self.protected_characteristics = [
            'race', 'gender', 'age', 'ethnicity', 'religion', 'disability_status',
            'sexual_orientation', 'national_origin', 'veteran_status', 'marital_status'
        ]

        # Fairness metrics definitions
        self.fairness_metrics = {
            'demographic_parity': {
                'description': 'Equal positive prediction rates across groups',
                'threshold': 0.8,  # 80% ratio threshold
                'critical_threshold': 0.6
            },
            'equalized_odds': {
                'description': 'Equal true positive and false positive rates across groups',
                'threshold': 0.8,
                'critical_threshold': 0.6
            },
            'calibration': {
                'description': 'Equal positive predictive value across groups',
                'threshold': 0.85,
                'critical_threshold': 0.7
            },
            'individual_fairness': {
                'description': 'Similar individuals receive similar outcomes',
                'threshold': 0.9,
                'critical_threshold': 0.75
            }
        }

        # Bias severity levels
        self.bias_severity_thresholds = {
            'critical': 0.6,
            'high': 0.7,
            'medium': 0.8,
            'low': 0.9
        }

    def detect_bias(self, system_context: Dict[str, Any],
                   performance_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive bias detection and analysis

        Args:
            system_context: AI system information including use case and deployment context
            performance_data: Optional system performance data for empirical analysis

        Returns:
            Comprehensive bias analysis with detected biases, severity, and mitigation strategies
        """
        try:
            detection_start = datetime.now()

            # Validate input
            if not self._validate_governance_input(['system_id', 'system_name', 'system_type'], system_context):
                raise ValueError("Missing required system information for bias detection")

            # Generate bias detection prompt
            bias_prompt = self._create_bias_detection_prompt(system_context, performance_data)

            # Get AI-powered bias analysis
            bias_analysis = self._generate_governance_response(bias_prompt, system_context)

            # Extract structured bias data
            structured_bias = self._extract_governance_data(bias_analysis, "bias_detection")

            # Assess bias risk across protected characteristics
            protected_group_analysis = self._assess_protected_group_bias(system_context, structured_bias)

            # Calculate fairness metrics
            fairness_assessment = self._calculate_fairness_metrics(system_context, structured_bias, performance_data)

            # Determine overall bias severity
            bias_severity = self._determine_bias_severity(protected_group_analysis, fairness_assessment)

            # Generate bias sources analysis
            bias_sources = self._analyze_bias_sources(system_context, structured_bias)

            # Generate mitigation strategies
            mitigation_strategies = self._generate_bias_mitigation_strategies(
                protected_group_analysis, fairness_assessment, bias_sources, system_context
            )

            # Calculate processing time
            processing_time = (datetime.now() - detection_start).total_seconds()

            # Create bias detection result
            detection_result = {
                'evaluation_id': self._create_assessment_id(),
                'system_id': system_context['system_id'],
                'evaluation_date': datetime.now().isoformat(),
                'bias_detected': bias_severity != 'none',
                'bias_severity': bias_severity,
                'protected_group_analysis': protected_group_analysis,
                'fairness_metrics': fairness_assessment,
                'bias_sources': bias_sources,
                'affected_groups': self._identify_affected_groups(protected_group_analysis),
                'mitigation_strategies': mitigation_strategies,
                'confidence_score': structured_bias.get('confidence_level', 7),
                'methodology': 'statistical_fairness_analysis',
                'processing_time_seconds': round(processing_time, 2),
                'requires_immediate_action': bias_severity in ['critical', 'high'],
                'bias_summary': self._generate_bias_summary(bias_severity, protected_group_analysis, fairness_assessment)
            }

            # Log bias detection interaction
            self._log_governance_interaction(
                system_context['system_id'],
                'bias_detection',
                {'input_context': system_context, 'performance_data': performance_data},
                detection_result,
                processing_time
            )

            return self._format_governance_response(bias_analysis, detection_result)

        except Exception as e:
            logger.error(f"Bias detection failed for system {system_context.get('system_id', 'unknown')}: {str(e)}")
            return self._format_governance_response(
                f"Bias detection failed due to technical error: {str(e)}",
                {'detection_status': 'failed', 'error': str(e)}
            )

    def _create_bias_detection_prompt(self, system_context: Dict[str, Any],
                                    performance_data: Optional[Dict[str, Any]]) -> str:
        """Create specialized bias detection prompt"""

        specific_instructions = f"""
BIAS DETECTION MISSION:
You are conducting comprehensive bias detection analysis for: {system_context['system_name']}

SYSTEM CONTEXT:
- Type: {system_context.get('system_type', 'Unknown')}
- Use Case: {system_context.get('description', 'Unknown')}
- Data Types: {system_context.get('data_types', [])}
- Users Affected: {system_context.get('users_affected', 'Unknown')}
- Decision Automation: {system_context.get('decision_automation', 'Unknown')}
- Business Impact: {system_context.get('business_impact', 'Unknown')}

BIAS ANALYSIS FRAMEWORK:
Analyze potential bias across these protected characteristics:
- Race/Ethnicity
- Gender/Sex
- Age
- Disability Status
- Religion
- Sexual Orientation
- National Origin
- Veteran Status

FAIRNESS METRICS TO EVALUATE:
1. DEMOGRAPHIC PARITY
   - Equal positive prediction rates across protected groups
   - Assess if system outcomes are distributed fairly
   - Flag disparities > 20% between groups

2. EQUALIZED ODDS
   - Equal true positive and false positive rates across groups
   - Evaluate if accuracy is consistent across demographics
   - Critical if disparities > 40%

3. CALIBRATION
   - Equal positive predictive value across groups
   - Assess if confidence scores mean the same across groups
   - Important for high-stakes decisions

4. INDIVIDUAL FAIRNESS
   - Similar individuals receive similar outcomes
   - Evaluate if similar cases are treated consistently
   - Critical for personalized systems

BIAS SOURCES TO IDENTIFY:
1. TRAINING DATA BIAS
   - Historical bias in datasets
   - Representation gaps across groups
   - Labeling bias and annotation errors
   - Sampling bias in data collection

2. ALGORITHMIC BIAS
   - Feature selection bias
   - Model architecture bias
   - Optimization objective bias
   - Proxy discrimination through correlated features

3. DEPLOYMENT BIAS
   - Usage pattern differences across groups
   - Feedback loop amplification
   - Context-dependent performance variations
   - User interaction bias

BIAS DETECTION REQUIREMENTS:
- Identify specific bias patterns and affected groups
- Quantify bias severity using fairness metrics
- Determine root causes and bias sources
- Assess impact on different stakeholder groups
- Generate specific, actionable mitigation strategies
- Consider legal and ethical implications

RISK ASSESSMENT CRITERIA:
- High-impact decisions (hiring, lending, healthcare)
- Large-scale deployment affecting diverse populations
- Automated decision-making with limited human oversight
- Historical discrimination in the application domain
- Regulatory compliance requirements (EEOC, EU AI Act)

OUTPUT REQUIREMENTS:
Provide comprehensive bias analysis including:
1. Bias detection findings with specific evidence
2. Affected protected groups and impact assessment
3. Fairness metric violations and severity
4. Root cause analysis of bias sources
5. Prioritized mitigation strategy recommendations
6. Compliance implications and legal risks
7. Monitoring recommendations for ongoing bias detection

Focus on actionable, implementable solutions that address identified biases while maintaining system performance.
"""

        return self._create_governance_prompt(specific_instructions)

    def _assess_protected_group_bias(self, system_context: Dict[str, Any],
                                   ai_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess bias across protected characteristics"""

        protected_group_analysis = {}

        for characteristic in self.protected_characteristics:
            # Determine relevance based on system type and context
            relevance = self._assess_characteristic_relevance(characteristic, system_context)

            if relevance['is_relevant']:
                bias_assessment = self._analyze_characteristic_bias(characteristic, system_context, ai_analysis)

                protected_group_analysis[characteristic] = {
                    'relevance': relevance,
                    'bias_detected': bias_assessment['bias_detected'],
                    'bias_score': bias_assessment['bias_score'],
                    'affected_subgroups': bias_assessment['affected_subgroups'],
                    'evidence': bias_assessment['evidence'],
                    'risk_level': self._determine_characteristic_risk_level(bias_assessment['bias_score'])
                }

        return protected_group_analysis

    def _assess_characteristic_relevance(self, characteristic: str, system_context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess relevance of protected characteristic for this system"""

        system_type = system_context.get('system_type', '')
        use_case_context = system_context.get('description', '').lower()

        # High relevance scenarios
        high_relevance_scenarios = {
            'race': ['hiring', 'lending', 'criminal justice', 'education', 'healthcare'],
            'gender': ['hiring', 'promotion', 'advertising', 'healthcare', 'insurance'],
            'age': ['hiring', 'insurance', 'healthcare', 'advertising', 'credit'],
            'disability_status': ['hiring', 'accommodation', 'accessibility', 'healthcare'],
            'religion': ['hiring', 'advertising', 'content moderation'],
            'sexual_orientation': ['hiring', 'advertising', 'healthcare', 'content moderation'],
            'national_origin': ['hiring', 'immigration', 'security screening'],
            'veteran_status': ['hiring', 'benefits', 'healthcare'],
            'marital_status': ['hiring', 'insurance', 'credit', 'benefits']
        }

        relevance_score = 5.0  # Base relevance

        # Check system type relevance
        if system_type in ['automated_decision_making', 'hiring_systems', 'credit_assessment']:
            relevance_score += 3.0
        elif system_type in ['recommendation_system', 'content_filtering']:
            relevance_score += 2.0

        # Check use case relevance
        for scenario in high_relevance_scenarios.get(characteristic, []):
            if scenario in use_case_context:
                relevance_score += 2.0
                break

        # Consider user scale impact
        users_affected = system_context.get('users_affected', 0)
        if users_affected > 100000:
            relevance_score += 1.0

        is_relevant = relevance_score >= 6.0

        return {
            'is_relevant': is_relevant,
            'relevance_score': min(10.0, relevance_score),
            'justification': self._get_relevance_justification(characteristic, system_context, is_relevant)
        }

    def _analyze_characteristic_bias(self, characteristic: str, system_context: Dict[str, Any],
                                   ai_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze bias for specific protected characteristic"""

        # Base bias score calculation
        bias_score = 0.8  # Default: minimal bias

        system_type = system_context.get('system_type', '')

        # High-risk system types for specific characteristics
        high_risk_mapping = {
            'race': ['hiring_systems', 'criminal_justice', 'credit_assessment'],
            'gender': ['hiring_systems', 'recommendation_system', 'advertising'],
            'age': ['hiring_systems', 'insurance', 'healthcare_ai'],
            'disability_status': ['hiring_systems', 'accessibility_systems'],
        }

        if system_type in high_risk_mapping.get(characteristic, []):
            bias_score -= 0.3

        # Decision automation impact
        automation_level = system_context.get('decision_automation', '')
        if automation_level in ['high', 'full']:
            bias_score -= 0.2
        elif automation_level == 'medium':
            bias_score -= 0.1

        # Human oversight impact (inverse)
        oversight = system_context.get('human_oversight', '')
        if oversight in ['none', 'limited']:
            bias_score -= 0.2
        elif oversight == 'moderate':
            bias_score -= 0.1

        # Scale impact
        users_affected = system_context.get('users_affected', 0)
        if users_affected > 1000000:
            bias_score -= 0.1

        bias_score = max(0.0, min(1.0, bias_score))
        bias_detected = bias_score < 0.8

        return {
            'bias_detected': bias_detected,
            'bias_score': bias_score,
            'affected_subgroups': self._identify_affected_subgroups(characteristic, bias_score),
            'evidence': self._generate_bias_evidence(characteristic, system_context, bias_score)
        }

    def _calculate_fairness_metrics(self, system_context: Dict[str, Any],
                                  structured_bias: Dict[str, Any],
                                  performance_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate fairness metrics assessment"""

        fairness_results = {}

        for metric_name, metric_config in self.fairness_metrics.items():
            # Simulate metric calculation (would use real performance data in production)
            metric_score = self._simulate_fairness_metric(metric_name, system_context, performance_data)

            # Determine compliance status
            if metric_score >= metric_config['threshold']:
                status = 'compliant'
                severity = 'low'
            elif metric_score >= metric_config['critical_threshold']:
                status = 'warning'
                severity = 'medium'
            else:
                status = 'violation'
                severity = 'high'

            fairness_results[metric_name] = {
                'score': metric_score,
                'threshold': metric_config['threshold'],
                'status': status,
                'severity': severity,
                'description': metric_config['description'],
                'recommendation': self._get_metric_recommendation(metric_name, status, metric_score)
            }

        return fairness_results

    def _determine_bias_severity(self, protected_group_analysis: Dict[str, Any],
                               fairness_assessment: Dict[str, Any]) -> str:
        """Determine overall bias severity level"""

        # Check for critical bias in protected groups
        critical_bias_count = sum(1 for analysis in protected_group_analysis.values()
                                if analysis.get('bias_score', 1.0) < self.bias_severity_thresholds['critical'])

        high_bias_count = sum(1 for analysis in protected_group_analysis.values()
                            if analysis.get('bias_score', 1.0) < self.bias_severity_thresholds['high'])

        # Check fairness metric violations
        fairness_violations = sum(1 for metric in fairness_assessment.values()
                                if metric.get('status') == 'violation')

        fairness_warnings = sum(1 for metric in fairness_assessment.values()
                              if metric.get('status') == 'warning')

        # Determine overall severity
        if critical_bias_count > 0 or fairness_violations >= 2:
            return 'critical'
        elif high_bias_count > 0 or fairness_violations >= 1:
            return 'high'
        elif fairness_warnings >= 2:
            return 'medium'
        elif fairness_warnings >= 1:
            return 'low'
        else:
            return 'none'

    def _analyze_bias_sources(self, system_context: Dict[str, Any],
                            structured_bias: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze potential sources of bias"""

        bias_sources = {
            'training_data': self._assess_training_data_bias(system_context),
            'algorithmic': self._assess_algorithmic_bias(system_context),
            'deployment': self._assess_deployment_bias(system_context),
            'feedback_loops': self._assess_feedback_loop_bias(system_context)
        }

        return bias_sources

    def _generate_bias_mitigation_strategies(self, protected_group_analysis: Dict[str, Any],
                                           fairness_assessment: Dict[str, Any],
                                           bias_sources: Dict[str, Any],
                                           system_context: Dict[str, Any]) -> List[str]:
        """Generate prioritized bias mitigation strategies"""

        strategies = []

        # Data-related mitigations
        if bias_sources.get('training_data', {}).get('risk_level') in ['high', 'critical']:
            strategies.extend([
                'Audit and rebalance training datasets for demographic representation',
                'Implement stratified sampling to ensure balanced group representation',
                'Apply data augmentation techniques to address underrepresented groups'
            ])

        # Algorithmic mitigations
        if bias_sources.get('algorithmic', {}).get('risk_level') in ['high', 'critical']:
            strategies.extend([
                'Implement fairness constraints in model optimization',
                'Apply bias correction techniques (reweighting, adversarial debiasing)',
                'Use fairness-aware feature selection methods'
            ])

        # Post-processing mitigations
        for metric_name, metric_result in fairness_assessment.items():
            if metric_result.get('status') in ['violation', 'warning']:
                strategies.append(f"Apply post-processing calibration to improve {metric_name}")

        # Monitoring and governance
        strategies.extend([
            'Implement continuous bias monitoring with demographic parity tracking',
            'Establish bias testing protocols for model updates',
            'Create bias incident response procedures'
        ])

        return strategies[:10]  # Limit to top 10 strategies

    def _generate_bias_summary(self, bias_severity: str, protected_group_analysis: Dict[str, Any],
                             fairness_assessment: Dict[str, Any]) -> str:
        """Generate human-readable bias analysis summary"""

        if bias_severity == 'none':
            return "No significant bias detected. Standard fairness monitoring recommended."

        affected_groups = [group for group, analysis in protected_group_analysis.items()
                          if analysis.get('bias_detected', False)]

        fairness_violations = [metric for metric, result in fairness_assessment.items()
                             if result.get('status') == 'violation']

        summary = f"Bias severity: {bias_severity.upper()}. "

        if affected_groups:
            summary += f"Potential bias detected for: {', '.join(affected_groups)}. "

        if fairness_violations:
            summary += f"Fairness violations: {', '.join(fairness_violations)}. "

        if bias_severity in ['critical', 'high']:
            summary += "Immediate bias mitigation required before deployment."
        elif bias_severity == 'medium':
            summary += "Enhanced bias monitoring and mitigation recommended."
        else:
            summary += "Standard bias monitoring protocols should be sufficient."

        return summary

    # Helper methods for bias analysis components
    def _assess_training_data_bias(self, system_context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess training data bias risk"""
        risk_score = 3.0  # Base score

        # Historical domains have higher training data bias risk
        high_bias_domains = ['hiring', 'lending', 'criminal justice', 'healthcare']
        use_case = system_context.get('description', '').lower()

        for domain in high_bias_domains:
            if domain in use_case:
                risk_score += 2.0
                break

        return {
            'risk_level': 'high' if risk_score >= 6.0 else 'medium' if risk_score >= 4.0 else 'low',
            'risk_score': min(10.0, risk_score),
            'factors': ['Historical bias in domain data', 'Representation gaps in training sets']
        }

    def _assess_algorithmic_bias(self, system_context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess algorithmic bias risk"""
        risk_score = 2.0  # Base score

        # Complex models have higher algorithmic bias risk
        complex_types = ['computer_vision', 'natural_language_processing', 'recommendation_system']
        if system_context.get('system_type') in complex_types:
            risk_score += 2.0

        # High automation increases risk
        if system_context.get('decision_automation') in ['high', 'full']:
            risk_score += 1.5

        return {
            'risk_level': 'high' if risk_score >= 5.0 else 'medium' if risk_score >= 3.5 else 'low',
            'risk_score': min(10.0, risk_score),
            'factors': ['Model complexity', 'Feature proxy discrimination', 'Optimization bias']
        }

    def _assess_deployment_bias(self, system_context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess deployment context bias risk"""
        risk_score = 2.0  # Base score

        # Large-scale deployment increases bias amplification risk
        users_affected = system_context.get('users_affected', 0)
        if users_affected > 1000000:
            risk_score += 2.0
        elif users_affected > 100000:
            risk_score += 1.0

        return {
            'risk_level': 'medium' if risk_score >= 4.0 else 'low',
            'risk_score': min(10.0, risk_score),
            'factors': ['Usage pattern differences', 'Context-dependent performance']
        }

    def _assess_feedback_loop_bias(self, system_context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess feedback loop bias risk"""
        risk_score = 1.0  # Base score

        # Recommendation and decision systems have higher feedback loop risk
        feedback_risk_types = ['recommendation_system', 'automated_decision_making']
        if system_context.get('system_type') in feedback_risk_types:
            risk_score += 3.0

        return {
            'risk_level': 'high' if risk_score >= 4.0 else 'medium' if risk_score >= 2.5 else 'low',
            'risk_score': min(10.0, risk_score),
            'factors': ['User interaction bias', 'Bias amplification cycles']
        }

    def _simulate_fairness_metric(self, metric_name: str, system_context: Dict[str, Any],
                                performance_data: Optional[Dict[str, Any]]) -> float:
        """Simulate fairness metric calculation (would use real data in production)"""

        # Base fairness score
        base_score = 0.85

        # Adjust based on system characteristics
        system_type = system_context.get('system_type', '')
        if system_type in ['automated_decision_making', 'hiring_systems']:
            base_score -= 0.15
        elif system_type in ['recommendation_system']:
            base_score -= 0.05

        # Adjust based on decision automation
        automation = system_context.get('decision_automation', '')
        if automation in ['high', 'full']:
            base_score -= 0.1

        # Add some variance by metric type
        metric_adjustments = {
            'demographic_parity': -0.05,
            'equalized_odds': -0.03,
            'calibration': 0.02,
            'individual_fairness': -0.08
        }

        base_score += metric_adjustments.get(metric_name, 0)

        return max(0.0, min(1.0, base_score))

    def _identify_affected_groups(self, protected_group_analysis: Dict[str, Any]) -> List[str]:
        """Identify groups affected by bias"""
        affected_groups = []

        for characteristic, analysis in protected_group_analysis.items():
            if analysis.get('bias_detected', False):
                affected_groups.extend(analysis.get('affected_subgroups', []))

        return list(set(affected_groups))

    def _identify_affected_subgroups(self, characteristic: str, bias_score: float) -> List[str]:
        """Identify specific subgroups affected by bias for a characteristic"""

        if bias_score >= 0.8:  # No significant bias
            return []

        # Common affected subgroups by characteristic
        subgroup_mapping = {
            'race': ['African American', 'Hispanic/Latino', 'Asian', 'Native American'],
            'gender': ['Women', 'Non-binary individuals'],
            'age': ['Older adults (50+)', 'Young adults (18-25)'],
            'disability_status': ['Individuals with disabilities'],
            'religion': ['Religious minorities'],
            'sexual_orientation': ['LGBTQ+ individuals'],
            'national_origin': ['Foreign-born individuals', 'Non-native speakers']
        }

        # Return potential affected groups (would be data-driven in production)
        potential_groups = subgroup_mapping.get(characteristic, [f'{characteristic} minorities'])

        # Return subset based on bias severity
        if bias_score < 0.6:  # High bias
            return potential_groups
        elif bias_score < 0.8:  # Medium bias
            return potential_groups[:2] if len(potential_groups) > 2 else potential_groups
        else:
            return []

    def _determine_characteristic_risk_level(self, bias_score: float) -> str:
        """Determine risk level for protected characteristic"""
        if bias_score < self.bias_severity_thresholds['critical']:
            return 'critical'
        elif bias_score < self.bias_severity_thresholds['high']:
            return 'high'
        elif bias_score < self.bias_severity_thresholds['medium']:
            return 'medium'
        else:
            return 'low'

    def _get_relevance_justification(self, characteristic: str, system_context: Dict[str, Any],
                                   is_relevant: bool) -> str:
        """Generate justification for characteristic relevance assessment"""
        if is_relevant:
            return f"{characteristic} is relevant due to system type and potential impact on protected groups"
        else:
            return f"{characteristic} has limited relevance for this system type and use case"

    def _generate_bias_evidence(self, characteristic: str, system_context: Dict[str, Any],
                              bias_score: float) -> List[str]:
        """Generate evidence for bias detection"""
        if bias_score >= 0.8:
            return ["No significant bias indicators detected"]

        evidence = []

        # System-based evidence
        if system_context.get('system_type') in ['automated_decision_making', 'hiring_systems']:
            evidence.append(f"High-risk system type for {characteristic} bias")

        if system_context.get('decision_automation') in ['high', 'full']:
            evidence.append("Limited human oversight increases bias risk")

        # Scale-based evidence
        if system_context.get('users_affected', 0) > 100000:
            evidence.append("Large-scale deployment amplifies potential bias impact")

        return evidence

    def _get_metric_recommendation(self, metric_name: str, status: str, score: float) -> str:
        """Get recommendation for fairness metric"""
        if status == 'compliant':
            return f"Continue monitoring {metric_name} to maintain fairness standards"
        elif status == 'warning':
            return f"Implement targeted interventions to improve {metric_name} (current: {score:.2f})"
        else:  # violation
            return f"Immediate action required to address {metric_name} violation (current: {score:.2f})"
