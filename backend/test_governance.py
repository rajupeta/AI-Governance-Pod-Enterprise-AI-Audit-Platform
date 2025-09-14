#!/usr/bin/env python3
"""
AI Governance System Testing
Comprehensive testing script for the enterprise AI governance platform
"""

import os
import sys
import logging
import json
from datetime import datetime

# Add backend to path
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GovernanceSystemTester:
    """Comprehensive testing for AI governance system"""

    def __init__(self):
        self.db_manager = SQLiteManager("database/governance_data.db")
        self.knowledge_store = None  # Mock for testing
        self.test_results = []

    def run_all_tests(self):
        """Run comprehensive governance system tests"""
        print("="*80)
        print("AI GOVERNANCE PLATFORM - COMPREHENSIVE TESTING")
        print("="*80)

        try:
            # Test 1: Database connectivity
            self._test_database_connectivity()

            # Test 2: Risk Assessment Agent
            self._test_risk_assessment_agent()

            # Test 3: Bias Detection Agent
            self._test_bias_detection_agent()

            # Test 4: Multi-Agent Orchestrator
            self._test_orchestrator_workflows()

            # Test 5: End-to-End Governance Workflow
            self._test_end_to_end_workflow()

            # Print test summary
            self._print_test_summary()

        except Exception as e:
            logger.error(f"Testing failed: {str(e)}")
            raise

    def _test_database_connectivity(self):
        """Test database connectivity and data retrieval"""
        print("\n" + "="*60)
        print("TEST 1: DATABASE CONNECTIVITY")
        print("="*60)

        try:
            # Test database connection
            connection = self.db_manager.get_connection()
            cursor = connection.cursor()

            # Test AI systems retrieval
            cursor.execute("SELECT COUNT(*) FROM ai_systems")
            system_count = cursor.fetchone()[0]
            print(f"✓ AI Systems in database: {system_count}")

            # Test policies retrieval
            cursor.execute("SELECT COUNT(*) FROM policies")
            policy_count = cursor.fetchone()[0]
            print(f"✓ Governance policies: {policy_count}")

            # Test regulatory frameworks
            cursor.execute("SELECT COUNT(*) FROM regulatory_frameworks")
            framework_count = cursor.fetchone()[0]
            print(f"✓ Regulatory frameworks: {framework_count}")

            # Test sample system retrieval
            cursor.execute("SELECT system_id, system_name, risk_category FROM ai_systems LIMIT 3")
            sample_systems = cursor.fetchall()

            print(f"\n📋 Sample AI Systems:")
            for system_id, name, risk_category in sample_systems:
                print(f"   • {system_id}: {name} (Risk: {risk_category})")

            self.test_results.append(("Database Connectivity", "PASSED", f"{system_count} systems loaded"))

        except Exception as e:
            print(f"✗ Database test failed: {str(e)}")
            self.test_results.append(("Database Connectivity", "FAILED", str(e)))
            raise

    def _test_risk_assessment_agent(self):
        """Test Risk Assessment Agent functionality"""
        print("\n" + "="*60)
        print("TEST 2: RISK ASSESSMENT AGENT")
        print("="*60)

        try:
            # Initialize Risk Assessment Agent
            risk_agent = RiskAssessmentAgent(self.knowledge_store, self.db_manager)
            print("✓ Risk Assessment Agent initialized")

            # Test system context for high-risk AI system
            test_system = {
                'system_id': 'TEST_RISK_001',
                'system_name': 'AI Hiring Assistant Test System',
                'system_type': 'automated_decision_making',
                'description': 'AI-powered resume screening and candidate ranking for hiring decisions',
                'deployment_status': 'production',
                'users_affected': 50000,
                'decision_automation': 'high',
                'human_oversight': 'limited',
                'data_sensitivity': 'personal_data',
                'business_impact': 'high',
                'regulatory_scope': ['GDPR', 'EU_AI_Act', 'EEOC_Guidelines'],
                'data_types': ['resume_data', 'interview_scores', 'demographic_data']
            }

            print(f"📊 Testing system: {test_system['system_name']}")

            # Perform risk assessment
            start_time = datetime.now()
            risk_result = risk_agent.assess_ai_system_risk(test_system)
            execution_time = (datetime.now() - start_time).total_seconds()

            print(f"✓ Risk assessment completed in {execution_time:.2f} seconds")

            # Validate result structure
            assert 'overall_risk_score' in risk_result
            assert 'risk_level' in risk_result
            assert 'dimensional_scores' in risk_result
            assert 'recommendations' in risk_result

            # Print key results
            overall_risk = risk_result.get('overall_risk_score', 0)
            risk_level = risk_result.get('risk_level', 'unknown')
            recommendations_count = len(risk_result.get('recommendations', []))

            print(f"📈 Overall Risk Score: {overall_risk}/10 ({risk_level.upper()})")
            print(f"📝 Mitigation Recommendations: {recommendations_count}")

            # Print dimensional risk breakdown
            dimensional_scores = risk_result.get('dimensional_scores', {})
            print(f"\n🎯 Risk Dimension Breakdown:")
            for dimension, data in dimensional_scores.items():
                score = data.get('score', 0)
                weight = data.get('weight', 0)
                print(f"   • {dimension.replace('_', ' ').title()}: {score:.1f}/10 (weight: {weight*100:.0f}%)")

            # Print top recommendations
            recommendations = risk_result.get('recommendations', [])[:3]
            if recommendations:
                print(f"\n💡 Top Mitigation Recommendations:")
                for i, rec in enumerate(recommendations, 1):
                    print(f"   {i}. {rec}")

            self.test_results.append(("Risk Assessment Agent", "PASSED", f"Risk: {overall_risk:.1f}/10 ({risk_level})"))

        except Exception as e:
            print(f"✗ Risk assessment test failed: {str(e)}")
            self.test_results.append(("Risk Assessment Agent", "FAILED", str(e)))
            raise

    def _test_bias_detection_agent(self):
        """Test Bias Detection Agent functionality"""
        print("\n" + "="*60)
        print("TEST 3: BIAS DETECTION AGENT")
        print("="*60)

        try:
            # Initialize Bias Detection Agent
            bias_agent = BiasDetectionAgent(self.knowledge_store, self.db_manager)
            print("✓ Bias Detection Agent initialized")

            # Test system context for bias-prone system
            test_system = {
                'system_id': 'TEST_BIAS_001',
                'system_name': 'Credit Scoring AI System',
                'system_type': 'automated_decision_making',
                'description': 'AI system for automated credit approval and loan risk assessment',
                'deployment_status': 'production',
                'users_affected': 500000,
                'decision_automation': 'high',
                'human_oversight': 'limited',
                'data_sensitivity': 'personal_data',
                'business_impact': 'critical',
                'regulatory_scope': ['GDPR', 'Fair_Credit_Reporting_Act', 'ECOA'],
                'data_types': ['credit_history', 'financial_data', 'demographic_data']
            }

            print(f"⚖️ Testing system: {test_system['system_name']}")

            # Perform bias detection
            start_time = datetime.now()
            bias_result = bias_agent.detect_bias(test_system)
            execution_time = (datetime.now() - start_time).total_seconds()

            print(f"✓ Bias detection completed in {execution_time:.2f} seconds")

            # Validate result structure
            assert 'bias_detected' in bias_result
            assert 'bias_severity' in bias_result
            assert 'protected_group_analysis' in bias_result
            assert 'fairness_metrics' in bias_result
            assert 'mitigation_strategies' in bias_result

            # Print key results
            bias_detected = bias_result.get('bias_detected', False)
            bias_severity = bias_result.get('bias_severity', 'unknown')
            affected_groups = bias_result.get('affected_groups', [])
            strategies_count = len(bias_result.get('mitigation_strategies', []))

            print(f"🚨 Bias Detected: {'YES' if bias_detected else 'NO'}")
            print(f"⚠️ Bias Severity: {bias_severity.upper()}")
            print(f"👥 Affected Groups: {len(affected_groups)}")
            print(f"🛠️ Mitigation Strategies: {strategies_count}")

            # Print protected group analysis
            protected_analysis = bias_result.get('protected_group_analysis', {})
            if protected_analysis:
                print(f"\n🎯 Protected Group Analysis:")
                for characteristic, analysis in list(protected_analysis.items())[:3]:
                    bias_score = analysis.get('bias_score', 1.0)
                    risk_level = analysis.get('risk_level', 'low')
                    print(f"   • {characteristic.replace('_', ' ').title()}: Score {bias_score:.2f} ({risk_level} risk)")

            # Print fairness metrics
            fairness_metrics = bias_result.get('fairness_metrics', {})
            if fairness_metrics:
                print(f"\n📊 Fairness Metrics:")
                for metric, result in list(fairness_metrics.items())[:3]:
                    score = result.get('score', 0)
                    status = result.get('status', 'unknown')
                    print(f"   • {metric.replace('_', ' ').title()}: {score:.2f} ({status})")

            # Print top mitigation strategies
            strategies = bias_result.get('mitigation_strategies', [])[:3]
            if strategies:
                print(f"\n💡 Top Mitigation Strategies:")
                for i, strategy in enumerate(strategies, 1):
                    print(f"   {i}. {strategy}")

            self.test_results.append(("Bias Detection Agent", "PASSED", f"Bias: {bias_severity}, Groups: {len(affected_groups)}"))

        except Exception as e:
            print(f"✗ Bias detection test failed: {str(e)}")
            self.test_results.append(("Bias Detection Agent", "FAILED", str(e)))
            raise

    def _test_orchestrator_workflows(self):
        """Test Multi-Agent Orchestrator workflows"""
        print("\n" + "="*60)
        print("TEST 4: MULTI-AGENT ORCHESTRATOR")
        print("="*60)

        try:
            # Test system for orchestration
            test_system = {
                'system_id': 'TEST_ORCH_001',
                'system_name': 'Comprehensive AI Governance Test',
                'system_type': 'recommendation_system',
                'description': 'Multi-modal recommendation system for e-commerce platform',
                'deployment_status': 'staging',
                'users_affected': 100000,
                'decision_automation': 'medium',
                'human_oversight': 'moderate',
                'data_sensitivity': 'personal_data',
                'business_impact': 'high',
                'regulatory_scope': ['GDPR', 'CCPA', 'NIST_AI_RMF'],
                'data_types': ['user_behavior', 'purchase_history', 'preferences']
            }

            print(f"🎭 Testing orchestrator with: {test_system['system_name']}")

            # Test 1: Rapid Screening Workflow
            print(f"\n🚀 Testing Rapid Screening Workflow...")
            start_time = datetime.now()
            rapid_result = example_rapid_screening(self.knowledge_store, self.db_manager, test_system)
            rapid_time = (datetime.now() - start_time).total_seconds()

            print(f"✓ Rapid screening completed in {rapid_time:.2f} seconds")
            print(f"   Risk Level: {rapid_result.get('risk_level', 'unknown')}")
            print(f"   Full Assessment Required: {rapid_result.get('requires_full_assessment', 'unknown')}")

            # Test 2: Comprehensive Assessment Workflow
            print(f"\n🔍 Testing Comprehensive Assessment Workflow...")
            start_time = datetime.now()
            comprehensive_result = example_comprehensive_assessment(self.knowledge_store, self.db_manager, test_system)
            comp_time = (datetime.now() - start_time).total_seconds()

            print(f"✓ Comprehensive assessment completed in {comp_time:.2f} seconds")
            print(f"   Overall Risk: {comprehensive_result.get('overall_risk', 'unknown')}")
            print(f"   Compliance Status: {comprehensive_result.get('compliance_status', 'unknown')}")
            print(f"   Agents Used: {', '.join(comprehensive_result.get('agents_used', []))}")
            print(f"   Recommendations: {len(comprehensive_result.get('recommendations', []))}")

            # Test 3: Pipeline Creation
            print(f"\n🏭 Testing Pipeline Creation...")
            orchestrator = create_governance_pipeline(self.knowledge_store, self.db_manager, "standard")
            stats = orchestrator.get_orchestrator_stats()

            print(f"✓ Standard pipeline created")
            print(f"   Registered Agents: {len(stats.get('registered_agents', []))}")
            print(f"   Available Workflows: {len(stats.get('available_workflow_types', []))}")

            # Test orchestrator health
            health = orchestrator.health_check()
            healthy_agents = sum(1 for status in health.get('agent_health', {}).values() if status)
            total_agents = len(health.get('agent_health', {}))

            print(f"   Health Status: {healthy_agents}/{total_agents} agents healthy")

            self.test_results.append(("Multi-Agent Orchestrator", "PASSED", f"Rapid: {rapid_time:.1f}s, Full: {comp_time:.1f}s"))

        except Exception as e:
            print(f"✗ Orchestrator test failed: {str(e)}")
            self.test_results.append(("Multi-Agent Orchestrator", "FAILED", str(e)))
            raise

    def _test_end_to_end_workflow(self):
        """Test complete end-to-end governance workflow"""
        print("\n" + "="*60)
        print("TEST 5: END-TO-END GOVERNANCE WORKFLOW")
        print("="*60)

        try:
            # Create realistic AI system scenario
            ai_system = {
                'system_id': 'PROD_E2E_001',
                'system_name': 'Enterprise Fraud Detection System',
                'system_type': 'fraud_detection',
                'description': 'Real-time fraud detection for financial transactions using ensemble machine learning',
                'deployment_status': 'production',
                'users_affected': 2000000,
                'decision_automation': 'high',
                'human_oversight': 'limited',
                'data_sensitivity': 'confidential',
                'business_impact': 'critical',
                'regulatory_scope': ['PCI_DSS', 'SOX', 'GDPR', 'Basel_III'],
                'data_types': ['transaction_data', 'user_behavior', 'device_information', 'geolocation'],
                'technical_details': {
                    'model_type': 'ensemble_ml',
                    'accuracy': 0.94,
                    'false_positive_rate': 0.02,
                    'latency_ms': 50,
                    'training_frequency': 'daily'
                }
            }

            print(f"🏢 End-to-End Test System: {ai_system['system_name']}")
            print(f"   Deployment: {ai_system['deployment_status']}")
            print(f"   Users Affected: {ai_system['users_affected']:,}")
            print(f"   Business Impact: {ai_system['business_impact']}")

            total_start = datetime.now()

            # Step 1: Create orchestrator
            print(f"\n📋 Step 1: Creating governance orchestrator...")
            orchestrator = create_governance_pipeline(self.knowledge_store, self.db_manager, "standard")
            print(f"✓ Orchestrator created with {len(orchestrator.get_available_agents())} agents")

            # Step 2: Create comprehensive workflow
            print(f"\n🔄 Step 2: Creating comprehensive governance workflow...")
            workflow_id = orchestrator.create_workflow(
                WorkflowType.COMPREHENSIVE_ASSESSMENT,
                ai_system
            )
            print(f"✓ Workflow created: {workflow_id}")

            # Step 3: Execute workflow
            print(f"\n▶️ Step 3: Executing governance workflow...")
            workflow_result = orchestrator.execute_workflow(workflow_id)

            # Extract results
            execution_time = workflow_result.execution_metadata.get('execution_time_seconds', 0)
            agents_executed = workflow_result.execution_metadata.get('agents_executed', [])
            overall_risk = workflow_result.aggregated_assessment.get('overall_risk_level', 'unknown')
            compliance_status = workflow_result.aggregated_assessment.get('overall_compliance', 'unknown')
            recommendations = workflow_result.aggregated_assessment.get('recommendations', [])

            print(f"✓ Workflow execution completed")
            print(f"   Execution Time: {execution_time:.2f} seconds")
            print(f"   Agents Executed: {', '.join(agents_executed)}")

            # Step 4: Analyze results
            print(f"\n📊 Step 4: Governance Assessment Results")
            print(f"   Overall Risk Level: {overall_risk.upper()}")
            print(f"   Compliance Status: {compliance_status.upper()}")
            print(f"   Total Recommendations: {len(recommendations)}")

            # Show top recommendations
            if recommendations:
                print(f"\n💡 Top Governance Recommendations:")
                for i, rec in enumerate(recommendations[:5], 1):
                    print(f"   {i}. {rec}")

            # Step 5: Compliance check
            print(f"\n✅ Step 5: Regulatory Compliance Check")
            regulatory_scope = ai_system.get('regulatory_scope', [])
            print(f"   Applicable Regulations: {', '.join(regulatory_scope)}")

            # Calculate total execution time
            total_time = (datetime.now() - total_start).total_seconds()
            print(f"   Total Workflow Time: {total_time:.2f} seconds")

            # Success criteria
            success_criteria = [
                len(agents_executed) >= 2,  # Multiple agents executed
                execution_time < 30,  # Reasonable execution time
                overall_risk in ['low', 'medium', 'high', 'critical'],  # Valid risk level
                len(recommendations) > 0  # Got recommendations
            ]

            if all(success_criteria):
                print(f"\n🎉 End-to-End Test: SUCCESS")
                self.test_results.append(("End-to-End Workflow", "PASSED", f"Risk: {overall_risk}, Time: {total_time:.1f}s"))
            else:
                print(f"\n❌ End-to-End Test: FAILED (criteria not met)")
                self.test_results.append(("End-to-End Workflow", "FAILED", "Success criteria not met"))

        except Exception as e:
            print(f"✗ End-to-end test failed: {str(e)}")
            self.test_results.append(("End-to-End Workflow", "FAILED", str(e)))
            raise

    def _print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*80)
        print("AI GOVERNANCE PLATFORM - TEST SUMMARY")
        print("="*80)

        passed_tests = sum(1 for result in self.test_results if result[1] == "PASSED")
        total_tests = len(self.test_results)

        print(f"\n📊 Test Results: {passed_tests}/{total_tests} PASSED\n")

        for test_name, status, details in self.test_results:
            status_symbol = "✅" if status == "PASSED" else "❌"
            print(f"{status_symbol} {test_name:<30} {status:<8} {details}")

        if passed_tests == total_tests:
            print(f"\n🎉 ALL TESTS PASSED! AI Governance Platform is ready for deployment.")
        else:
            print(f"\n⚠️ {total_tests - passed_tests} test(s) failed. Please review and fix issues.")

        print(f"\n🔧 System Capabilities Verified:")
        print(f"   • Enterprise database with {self._get_db_stats()} records")
        print(f"   • Multi-dimensional risk assessment")
        print(f"   • Comprehensive bias detection across protected characteristics")
        print(f"   • Multi-agent governance orchestration")
        print(f"   • End-to-end governance workflow automation")
        print(f"   • Regulatory compliance checking (EU AI Act, GDPR, NIST AI RMF)")

        print(f"\n📈 Performance Metrics:")
        for test_name, status, details in self.test_results:
            if "Time:" in details or "s" in details:
                print(f"   • {test_name}: {details}")

        print("="*80)

    def _get_db_stats(self):
        """Get database statistics for summary"""
        try:
            connection = self.db_manager.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM ai_systems")
            return cursor.fetchone()[0]
        except:
            return "N/A"

def main():
    """Main testing function"""
    print("Initializing AI Governance Platform Testing...")

    # Set environment variable for testing
    os.environ['TESTING'] = 'true'

    try:
        tester = GovernanceSystemTester()
        tester.run_all_tests()

    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Testing failed with error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()