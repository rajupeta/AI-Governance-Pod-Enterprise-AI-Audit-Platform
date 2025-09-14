#!/usr/bin/env python3
"""
AI Governance Database Initialization
Creates and populates the enterprise governance database with comprehensive test data
"""

import sqlite3
import os
import json
import logging
from datetime import datetime, timedelta
import random
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GovernanceDatabaseInitializer:
    """Initialize comprehensive governance database with realistic enterprise data"""

    def __init__(self, db_path="database/governance_data.db"):
        self.db_path = db_path
        self.connection = None

    def initialize_database(self):
        """Complete database initialization process"""
        try:
            logger.info("Starting AI Governance Database initialization...")

            # Create database directory if it doesn't exist
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

            # Connect to database
            self.connection = sqlite3.connect(self.db_path)
            self.connection.execute("PRAGMA foreign_keys = ON")

            # Create schema
            self._create_schema()

            # Populate with seed data
            self._populate_base_data()

            # Generate additional enterprise data
            self._generate_enterprise_systems()
            self._generate_assessment_history()
            self._generate_compliance_data()
            self._generate_monitoring_data()

            # Commit all changes
            self.connection.commit()

            logger.info(f"Database initialization completed successfully at {self.db_path}")
            self._print_database_stats()

        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            raise
        finally:
            if self.connection:
                self.connection.close()

    def _create_schema(self):
        """Create database schema from SQL file"""
        logger.info("Creating database schema...")

        with open("database/schema.sql", "r") as f:
            schema_sql = f.read()

        # Execute schema creation
        self.connection.executescript(schema_sql)
        logger.info("Schema created successfully")

    def _populate_base_data(self):
        """Populate database with base seed data"""
        logger.info("Populating base seed data...")

        with open("database/seed_data.sql", "r") as f:
            seed_sql = f.read()

        # Execute seed data insertion
        self.connection.executescript(seed_sql)
        logger.info("Base seed data populated successfully")

    def _generate_enterprise_systems(self):
        """Generate additional AI systems to reach 200 total systems"""
        logger.info("Generating additional enterprise AI systems...")

        system_types = [
            'recommendation_system', 'risk_assessment', 'automated_decision_making',
            'content_filtering', 'medical_ai', 'computer_vision', 'natural_language_processing',
            'predictive_analytics', 'chatbot', 'image_recognition', 'fraud_detection',
            'sentiment_analysis', 'optimization_engine', 'forecasting_system', 'classification_system'
        ]

        business_units = [
            'E-commerce', 'Financial Services', 'Healthcare', 'Manufacturing', 'Retail',
            'Media & Entertainment', 'Telecommunications', 'Automotive', 'Energy', 'Education',
            'Government', 'Insurance', 'Real Estate', 'Transportation', 'Cybersecurity'
        ]

        teams = [
            'Data Science Team', 'AI/ML Engineering', 'Product Engineering', 'Risk Management',
            'Compliance Team', 'Security Team', 'Operations Team', 'Research Team', 'Platform Team'
        ]

        # Generate 195 additional systems (5 already exist in seed data)
        systems_to_generate = 195

        for i in range(6, systems_to_generate + 6):  # Starting from SYS_006
            system_id = f"SYS_{i:03d}"
            system_name = self._generate_system_name(system_types, i)
            system_type = random.choice(system_types)
            description = self._generate_system_description(system_name, system_type)
            risk_category = random.choices(['low', 'medium', 'high', 'critical'], weights=[30, 40, 25, 5])[0]
            deployment_status = random.choices(['development', 'testing', 'staging', 'production', 'deprecated'],
                                             weights=[10, 15, 10, 60, 5])[0]
            owner_team = random.choice(teams)
            business_unit = random.choice(business_units)

            # Generate realistic data types
            data_types = self._generate_data_types(system_type)
            users_affected = random.randint(100, 500000)
            decision_automation = random.choices(['none', 'low', 'medium', 'high', 'full'],
                                                weights=[10, 20, 30, 30, 10])[0]
            human_oversight = random.choices(['none', 'limited', 'moderate', 'extensive', 'full'],
                                           weights=[5, 20, 35, 30, 10])[0]
            data_sensitivity = random.choices(['public', 'internal', 'confidential', 'personal_data', 'sensitive_personal'],
                                            weights=[10, 25, 30, 25, 10])[0]
            business_impact = random.choices(['low', 'medium', 'high', 'critical'], weights=[20, 40, 30, 10])[0]

            # Generate regulatory scope
            regulatory_scope = self._generate_regulatory_scope(system_type, data_sensitivity)

            # Generate technical details
            technical_details = self._generate_technical_details(system_type)

            # Generate governance score
            governance_score = round(random.uniform(3.0, 9.5), 1)

            # Generate compliance status
            compliance_status = random.choices(['compliant', 'partially_compliant', 'non_compliant', 'unknown'],
                                             weights=[40, 35, 15, 10])[0]

            # Generate dates
            created_date = datetime.now() - timedelta(days=random.randint(30, 730))
            last_assessment = created_date + timedelta(days=random.randint(1, 180))

            # Insert system
            self.connection.execute("""
                INSERT INTO ai_systems VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                system_id, system_name, system_type, description, risk_category, deployment_status,
                owner_team, business_unit, json.dumps(data_types), users_affected, decision_automation,
                human_oversight, data_sensitivity, business_impact, json.dumps(regulatory_scope),
                json.dumps(technical_details), last_assessment.isoformat(), governance_score,
                compliance_status, created_date.isoformat(), datetime.now().isoformat()
            ))

        logger.info(f"Generated {systems_to_generate} additional AI systems")

    def _generate_assessment_history(self):
        """Generate comprehensive risk assessment history"""
        logger.info("Generating risk assessment history...")

        # Get all systems
        cursor = self.connection.execute("SELECT system_id FROM ai_systems")
        systems = [row[0] for row in cursor.fetchall()]

        assessment_count = 0
        for system_id in systems:
            # Generate 2-5 assessments per system
            num_assessments = random.randint(2, 5)

            for i in range(num_assessments):
                assessment_id = f"{system_id}_RISK_{i+1}_{uuid.uuid4().hex[:8]}"
                assessment_date = datetime.now() - timedelta(days=random.randint(30, 365))
                assessor_id = f"assessor_{random.randint(1, 20):03d}"
                assessment_type = random.choices(['initial', 'periodic', 'change_triggered', 'incident_response'],
                                               weights=[20, 50, 25, 5])[0]

                # Generate risk scores
                overall_risk = round(random.uniform(2.0, 9.0), 1)
                bias_risk = round(random.uniform(1.0, 8.0), 1)
                privacy_risk = round(random.uniform(2.0, 9.0), 1)
                security_risk = round(random.uniform(3.0, 8.5), 1)
                explainability_risk = round(random.uniform(2.0, 7.0), 1)
                regulatory_risk = round(random.uniform(3.0, 8.0), 1)

                # Generate risk factors and recommendations
                risk_factors = self._generate_risk_factors(overall_risk)
                risk_categories = self._generate_risk_categories(bias_risk, privacy_risk, security_risk)
                recommendations = self._generate_recommendations(overall_risk, risk_factors)

                confidence_level = round(random.uniform(6.0, 9.5), 1)
                methodology = random.choice(['quantitative_analysis', 'qualitative_assessment', 'hybrid_approach', 'automated_scanning'])
                review_required = overall_risk >= 7.0 or bias_risk >= 7.0

                approved_by = f"manager_{random.randint(1, 10):03d}" if not review_required else None
                approval_date = (assessment_date + timedelta(days=random.randint(1, 7))).isoformat() if approved_by else None

                self.connection.execute("""
                    INSERT INTO risk_assessments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    assessment_id, system_id, assessment_date.isoformat(), assessor_id, assessment_type,
                    overall_risk, bias_risk, privacy_risk, security_risk, explainability_risk, regulatory_risk,
                    json.dumps(risk_factors), json.dumps(risk_categories), json.dumps(recommendations),
                    confidence_level, methodology, review_required, approved_by, approval_date
                ))

                assessment_count += 1

        logger.info(f"Generated {assessment_count} risk assessments")

    def _generate_compliance_data(self):
        """Generate comprehensive compliance check data"""
        logger.info("Generating compliance check data...")

        # Get all systems and policies
        cursor = self.connection.execute("SELECT system_id FROM ai_systems")
        systems = [row[0] for row in cursor.fetchall()]

        cursor = self.connection.execute("SELECT policy_id FROM policies")
        policies = [row[0] for row in cursor.fetchall()]

        compliance_count = 0
        for system_id in systems:
            # Each system gets checked against 2-4 policies
            num_checks = random.randint(2, 4)
            selected_policies = random.sample(policies, min(num_checks, len(policies)))

            for policy_id in selected_policies:
                check_id = f"{system_id}_{policy_id}_CHECK_{uuid.uuid4().hex[:8]}"
                check_date = datetime.now() - timedelta(days=random.randint(1, 180))
                checker_id = f"checker_{random.randint(1, 15):03d}"
                check_type = random.choices(['automated', 'manual', 'hybrid'], weights=[50, 30, 20])[0]

                compliance_status = random.choices(['compliant', 'partially_compliant', 'non_compliant', 'not_applicable'],
                                                 weights=[50, 25, 20, 5])[0]
                compliance_score = self._generate_compliance_score(compliance_status)

                findings = self._generate_compliance_findings(compliance_status)
                evidence = self._generate_compliance_evidence(compliance_status)
                gaps = self._generate_compliance_gaps(compliance_status)

                remediation_required = compliance_status in ['partially_compliant', 'non_compliant']
                remediation_plan = self._generate_remediation_plan(compliance_status) if remediation_required else None
                remediation_deadline = (check_date + timedelta(days=random.randint(30, 90))).isoformat() if remediation_required else None
                remediation_status = random.choice(['planned', 'in_progress', 'completed']) if remediation_required else 'not_required'
                next_check_date = (check_date + timedelta(days=random.randint(90, 365))).isoformat()

                self.connection.execute("""
                    INSERT INTO compliance_checks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    check_id, system_id, policy_id, check_date.isoformat(), checker_id, check_type,
                    compliance_status, compliance_score, json.dumps(findings), json.dumps(evidence),
                    json.dumps(gaps), remediation_required, remediation_plan, remediation_deadline,
                    remediation_status, next_check_date
                ))

                compliance_count += 1

        logger.info(f"Generated {compliance_count} compliance checks")

    def _generate_monitoring_data(self):
        """Generate monitoring metrics data"""
        logger.info("Generating monitoring metrics...")

        cursor = self.connection.execute("SELECT system_id FROM ai_systems WHERE deployment_status = 'production'")
        production_systems = [row[0] for row in cursor.fetchall()]

        metric_types = [
            'accuracy', 'precision', 'recall', 'f1_score', 'auc_roc', 'bias_score', 'fairness_metric',
            'response_time', 'throughput', 'error_rate', 'availability', 'data_drift', 'model_drift',
            'prediction_confidence', 'feature_importance_stability'
        ]

        metric_count = 0
        for system_id in production_systems:
            # Generate metrics for last 90 days
            for days_ago in range(0, 90, 7):  # Weekly metrics
                measurement_date = datetime.now() - timedelta(days=days_ago)

                # Generate 3-8 different metrics per measurement
                num_metrics = random.randint(3, 8)
                selected_metrics = random.sample(metric_types, num_metrics)

                for metric_name in selected_metrics:
                    metric_id = f"{system_id}_{metric_name}_{measurement_date.strftime('%Y%m%d')}_{uuid.uuid4().hex[:6]}"
                    metric_category = self._get_metric_category(metric_name)
                    metric_value, metric_unit = self._generate_metric_value(metric_name)
                    threshold_value, threshold_type = self._generate_metric_threshold(metric_name, metric_value)
                    threshold_status = self._determine_threshold_status(metric_value, threshold_value, threshold_type)

                    alert_triggered = threshold_status in ['warning', 'critical', 'breach']
                    alert_level = 'info' if not alert_triggered else threshold_status
                    remediation_triggered = threshold_status == 'breach'

                    measurement_method = random.choice(['automated_monitoring', 'batch_analysis', 'real_time_tracking'])
                    measurement_context = json.dumps({
                        'system_load': random.uniform(0.1, 0.9),
                        'data_volume': random.randint(1000, 50000),
                        'time_period': '7_days'
                    })

                    self.connection.execute("""
                        INSERT INTO monitoring_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        metric_id, system_id, measurement_date.isoformat(), metric_name, metric_category,
                        metric_name, metric_value, metric_unit, threshold_value, threshold_type,
                        threshold_status, measurement_method, measurement_context, alert_triggered,
                        alert_level, remediation_triggered, None
                    ))

                    metric_count += 1

        logger.info(f"Generated {metric_count} monitoring metrics")

    # Helper methods for data generation
    def _generate_system_name(self, system_types, index):
        """Generate realistic system names"""
        prefixes = ['Enterprise', 'Advanced', 'Smart', 'Intelligent', 'Automated', 'Predictive', 'Real-time', 'Dynamic']
        suffixes = ['Engine', 'Platform', 'System', 'Service', 'Assistant', 'Analyzer', 'Optimizer', 'Monitor']

        type_names = {
            'recommendation_system': 'Recommendation',
            'risk_assessment': 'Risk Assessment',
            'automated_decision_making': 'Decision',
            'content_filtering': 'Content Filter',
            'medical_ai': 'Medical AI',
            'computer_vision': 'Vision',
            'natural_language_processing': 'NLP',
            'predictive_analytics': 'Predictive Analytics',
            'chatbot': 'Chatbot',
            'image_recognition': 'Image Recognition',
            'fraud_detection': 'Fraud Detection',
            'sentiment_analysis': 'Sentiment Analysis',
            'optimization_engine': 'Optimization',
            'forecasting_system': 'Forecasting',
            'classification_system': 'Classification'
        }

        system_type = random.choice(list(system_types))
        prefix = random.choice(prefixes)
        type_name = type_names.get(system_type, 'AI')
        suffix = random.choice(suffixes)

        return f"{prefix} {type_name} {suffix} v{random.randint(1, 5)}.{random.randint(0, 9)}"

    def _generate_system_description(self, name, system_type):
        """Generate realistic system descriptions"""
        descriptions = {
            'recommendation_system': 'Provides personalized recommendations using machine learning algorithms',
            'risk_assessment': 'Automated risk evaluation and scoring system for business decisions',
            'automated_decision_making': 'AI-powered decision automation for operational efficiency',
            'content_filtering': 'Intelligent content moderation and filtering system',
            'medical_ai': 'AI-assisted medical diagnosis and treatment recommendation system',
            'computer_vision': 'Computer vision system for image and video analysis',
            'natural_language_processing': 'NLP system for text analysis and understanding',
            'predictive_analytics': 'Predictive modeling system for business forecasting',
            'chatbot': 'Conversational AI for customer service and support',
            'image_recognition': 'Image classification and object detection system',
            'fraud_detection': 'Real-time fraud detection and prevention system',
            'sentiment_analysis': 'Text sentiment analysis and emotion detection system',
            'optimization_engine': 'AI-powered optimization for resource allocation',
            'forecasting_system': 'Time series forecasting and prediction system',
            'classification_system': 'Multi-class classification system for data categorization'
        }

        base_description = descriptions.get(system_type, 'AI system for automated processing')
        return f"{name} - {base_description} with enterprise-grade security and compliance features"

    def _generate_data_types(self, system_type):
        """Generate realistic data types for different system types"""
        data_type_mappings = {
            'recommendation_system': ['user_behavior', 'purchase_history', 'product_metadata', 'ratings'],
            'risk_assessment': ['financial_data', 'transaction_history', 'user_profiles', 'market_data'],
            'automated_decision_making': ['business_rules', 'historical_decisions', 'performance_metrics'],
            'content_filtering': ['user_content', 'moderation_history', 'reporting_data'],
            'medical_ai': ['medical_images', 'patient_records', 'clinical_data', 'diagnostic_history'],
            'computer_vision': ['images', 'video_data', 'metadata', 'annotations'],
            'natural_language_processing': ['text_data', 'documents', 'conversation_logs'],
            'predictive_analytics': ['historical_data', 'market_indicators', 'performance_metrics'],
            'chatbot': ['conversation_data', 'user_queries', 'response_history'],
            'image_recognition': ['image_data', 'labeled_datasets', 'feature_vectors'],
            'fraud_detection': ['transaction_data', 'user_behavior', 'device_information'],
            'sentiment_analysis': ['text_content', 'social_media_data', 'reviews'],
            'optimization_engine': ['operational_data', 'resource_metrics', 'constraints'],
            'forecasting_system': ['time_series_data', 'external_factors', 'seasonal_patterns'],
            'classification_system': ['labeled_data', 'feature_sets', 'training_examples']
        }

        return data_type_mappings.get(system_type, ['general_data', 'metadata'])

    def _generate_regulatory_scope(self, system_type, data_sensitivity):
        """Generate applicable regulatory frameworks"""
        base_regulations = []

        if data_sensitivity in ['personal_data', 'sensitive_personal']:
            base_regulations.extend(['GDPR', 'CCPA'])

        if system_type in ['medical_ai']:
            base_regulations.extend(['HIPAA', 'FDA_510k', 'MDR'])
        elif system_type in ['fraud_detection', 'risk_assessment']:
            base_regulations.extend(['PCI_DSS', 'SOX', 'Basel_III'])
        elif system_type in ['automated_decision_making', 'hiring_systems']:
            base_regulations.extend(['EU_AI_Act', 'EEOC_Guidelines'])

        # Add general AI regulations
        base_regulations.extend(['NIST_AI_RMF', 'ISO_42001'])

        return list(set(base_regulations))

    def _generate_technical_details(self, system_type):
        """Generate realistic technical specifications"""
        model_types = {
            'recommendation_system': 'collaborative_filtering',
            'risk_assessment': 'ensemble_model',
            'automated_decision_making': 'decision_tree',
            'content_filtering': 'transformer_based',
            'medical_ai': 'convolutional_neural_network',
            'computer_vision': 'deep_cnn',
            'natural_language_processing': 'transformer',
            'predictive_analytics': 'time_series_model',
            'chatbot': 'sequence_to_sequence',
            'image_recognition': 'resnet_architecture',
            'fraud_detection': 'gradient_boosting',
            'sentiment_analysis': 'bert_based',
            'optimization_engine': 'genetic_algorithm',
            'forecasting_system': 'lstm_network',
            'classification_system': 'random_forest'
        }

        return {
            'model_type': model_types.get(system_type, 'machine_learning'),
            'training_frequency': random.choice(['daily', 'weekly', 'monthly', 'quarterly']),
            'model_size_mb': random.randint(10, 500),
            'feature_count': random.randint(20, 1000),
            'accuracy': round(random.uniform(0.75, 0.98), 3),
            'latency_ms': random.randint(10, 1000),
            'throughput_rps': random.randint(100, 10000)
        }

    def _generate_risk_factors(self, overall_risk):
        """Generate risk factors based on overall risk score"""
        all_factors = [
            'data_quality_issues', 'model_bias', 'privacy_concerns', 'security_vulnerabilities',
            'algorithmic_transparency', 'regulatory_compliance', 'operational_risks', 'ethical_concerns',
            'performance_degradation', 'data_drift', 'model_drift', 'adversarial_attacks',
            'insufficient_monitoring', 'lack_of_explainability', 'stakeholder_concerns'
        ]

        # Higher risk systems have more factors
        num_factors = min(int(overall_risk / 2) + 2, len(all_factors))
        return random.sample(all_factors, num_factors)

    def _generate_risk_categories(self, bias_risk, privacy_risk, security_risk):
        """Generate categorized risk assessment"""
        return {
            'bias': {'score': bias_risk, 'factors': ['demographic_bias', 'algorithmic_bias']},
            'privacy': {'score': privacy_risk, 'factors': ['data_exposure', 'consent_issues']},
            'security': {'score': security_risk, 'factors': ['access_control', 'data_protection']},
            'operational': {'score': round(random.uniform(2.0, 7.0), 1), 'factors': ['system_reliability', 'performance']}
        }

    def _generate_recommendations(self, overall_risk, risk_factors):
        """Generate mitigation recommendations"""
        recommendation_map = {
            'data_quality_issues': 'Implement data quality monitoring and validation',
            'model_bias': 'Conduct bias testing and implement fairness constraints',
            'privacy_concerns': 'Enhance privacy protection measures and consent management',
            'security_vulnerabilities': 'Strengthen security controls and access management',
            'algorithmic_transparency': 'Improve model explainability and documentation',
            'regulatory_compliance': 'Ensure compliance with applicable regulations',
            'operational_risks': 'Implement robust monitoring and incident response',
            'ethical_concerns': 'Establish ethical review board and guidelines'
        }

        recommendations = []
        for factor in risk_factors[:5]:  # Limit to top 5 recommendations
            if factor in recommendation_map:
                recommendations.append(recommendation_map[factor])

        return recommendations

    def _generate_compliance_score(self, status):
        """Generate compliance score based on status"""
        if status == 'compliant':
            return round(random.uniform(8.0, 10.0), 1)
        elif status == 'partially_compliant':
            return round(random.uniform(5.0, 7.9), 1)
        elif status == 'non_compliant':
            return round(random.uniform(1.0, 4.9), 1)
        else:  # not_applicable
            return None

    def _generate_compliance_findings(self, status):
        """Generate compliance findings"""
        findings_map = {
            'compliant': ['All requirements met', 'Documentation complete', 'Controls effective'],
            'partially_compliant': ['Some gaps identified', 'Documentation needs improvement', 'Additional controls needed'],
            'non_compliant': ['Major violations found', 'Critical gaps in compliance', 'Immediate action required'],
            'not_applicable': ['Policy not applicable to this system']
        }

        return findings_map.get(status, [])

    def _generate_compliance_evidence(self, status):
        """Generate compliance evidence"""
        if status == 'not_applicable':
            return []

        evidence_types = ['policy_documentation', 'audit_reports', 'test_results', 'training_records', 'approval_documents']
        num_evidence = random.randint(1, 4) if status == 'compliant' else random.randint(0, 2)
        return random.sample(evidence_types, min(num_evidence, len(evidence_types)))

    def _generate_compliance_gaps(self, status):
        """Generate compliance gaps"""
        if status in ['compliant', 'not_applicable']:
            return []

        gap_types = ['missing_documentation', 'insufficient_controls', 'training_gaps', 'process_weaknesses', 'technology_limitations']
        num_gaps = random.randint(1, 3) if status == 'partially_compliant' else random.randint(2, 5)
        return random.sample(gap_types, min(num_gaps, len(gap_types)))

    def _generate_remediation_plan(self, status):
        """Generate remediation plan"""
        if status == 'partially_compliant':
            return 'Address identified gaps and improve documentation within 60 days'
        elif status == 'non_compliant':
            return 'Immediate remediation required - implement critical controls and conduct compliance review'
        return None

    def _get_metric_category(self, metric_name):
        """Get category for metric type"""
        category_map = {
            'accuracy': 'performance', 'precision': 'performance', 'recall': 'performance', 'f1_score': 'performance',
            'auc_roc': 'performance', 'bias_score': 'bias', 'fairness_metric': 'fairness',
            'response_time': 'performance', 'throughput': 'performance', 'error_rate': 'performance',
            'availability': 'performance', 'data_drift': 'bias', 'model_drift': 'performance',
            'prediction_confidence': 'explainability', 'feature_importance_stability': 'explainability'
        }
        return category_map.get(metric_name, 'performance')

    def _generate_metric_value(self, metric_name):
        """Generate realistic metric values"""
        value_ranges = {
            'accuracy': (0.75, 0.98, None), 'precision': (0.70, 0.95, None), 'recall': (0.65, 0.92, None),
            'f1_score': (0.70, 0.94, None), 'auc_roc': (0.75, 0.99, None), 'bias_score': (0.0, 1.0, None),
            'fairness_metric': (0.6, 1.0, None), 'response_time': (10, 1000, 'ms'), 'throughput': (100, 5000, 'rps'),
            'error_rate': (0.001, 0.05, '%'), 'availability': (0.95, 0.999, '%'), 'data_drift': (0.0, 0.3, None),
            'model_drift': (0.0, 0.2, None), 'prediction_confidence': (0.7, 0.95, None),
            'feature_importance_stability': (0.8, 1.0, None)
        }

        min_val, max_val, unit = value_ranges.get(metric_name, (0, 100, None))
        value = round(random.uniform(min_val, max_val), 3)
        return value, unit

    def _generate_metric_threshold(self, metric_name, current_value):
        """Generate threshold for metric"""
        # Threshold is typically 80-95% of current value for performance metrics
        if metric_name in ['accuracy', 'precision', 'recall', 'f1_score', 'availability']:
            threshold = round(current_value * random.uniform(0.85, 0.95), 3)
            return threshold, 'minimum'
        elif metric_name in ['response_time', 'error_rate', 'bias_score', 'data_drift', 'model_drift']:
            threshold = round(current_value * random.uniform(1.1, 1.5), 3)
            return threshold, 'maximum'
        else:
            threshold = round(current_value * random.uniform(0.9, 1.1), 3)
            return threshold, 'range'

    def _determine_threshold_status(self, value, threshold, threshold_type):
        """Determine if metric is within threshold"""
        if threshold_type == 'minimum':
            if value >= threshold:
                return 'within_threshold'
            elif value >= threshold * 0.9:
                return 'warning'
            else:
                return 'breach'
        elif threshold_type == 'maximum':
            if value <= threshold:
                return 'within_threshold'
            elif value <= threshold * 1.1:
                return 'warning'
            else:
                return 'breach'
        else:  # range
            if abs(value - threshold) <= threshold * 0.1:
                return 'within_threshold'
            elif abs(value - threshold) <= threshold * 0.2:
                return 'warning'
            else:
                return 'breach'

    def _print_database_stats(self):
        """Print database statistics"""
        tables = [
            'ai_systems', 'risk_assessments', 'policies', 'compliance_checks',
            'audit_events', 'bias_evaluations', 'regulatory_frameworks', 'monitoring_metrics'
        ]

        print("\n" + "="*50)
        print("AI GOVERNANCE DATABASE STATISTICS")
        print("="*50)

        for table in tables:
            cursor = self.connection.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table.replace('_', ' ').title():<30}: {count:>6}")

        print("="*50)
        print("Database initialization completed successfully!")
        print("="*50)

def main():
    """Main initialization function"""
    initializer = GovernanceDatabaseInitializer()
    initializer.initialize_database()

if __name__ == "__main__":
    main()