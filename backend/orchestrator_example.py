#!/usr/bin/env python3
"""
AI Governance Orchestrator - Integration Example
Demonstrates how to use the orchestrator pattern for coordinated AI governance assessments
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any

# Import orchestrator components
from agents import (
    create_governance_pipeline,
    WorkflowType,
    example_comprehensive_assessment,
    example_rapid_screening,
    example_custom_workflow,
    WorkflowBuilder
)

# Mock database classes for the example
class MockKnowledgeStore:
    """Mock knowledge store for demonstration"""
    def health_check(self):
        return True

class MockGovernanceDB:
    """Mock governance database for demonstration"""
    def health_check(self):
        return True

    def log_audit_event(self, system_id: str, action: str, details: str):
        print(f"[AUDIT] {system_id}: {action} - {details}")

def main():
    """Demonstrate orchestrator usage patterns"""

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    print("=== AI Governance Orchestrator Demo ===\n")

    # Initialize mock dependencies
    knowledge_store = MockKnowledgeStore()
    governance_db = MockGovernanceDB()

    # Example AI system to assess
    ai_system_context = {
        "system_id": "recommendation_engine_v2",
        "system_name": "E-commerce Recommendation System",
        "description": "Machine learning system that provides personalized product recommendations",
        "risk_category": "medium",
        "data_types": ["user_behavior", "purchase_history", "demographic_data"],
        "deployment": "production",
        "users_affected": 100000,
        "decision_automation": "high",
        "human_oversight": "limited",
        "data_sensitivity": "personal_data",
        "business_impact": "high",
        "regulatory_scope": ["GDPR", "CCPA"],
        "technical_details": {
            "model_type": "collaborative_filtering",
            "training_data_size": "10M_records",
            "update_frequency": "daily",
            "accuracy_metrics": {"precision": 0.85, "recall": 0.78}
        }
    }

    print("Assessing AI System:")
    print(json.dumps(ai_system_context, indent=2))
    print("\n" + "="*60 + "\n")

    # Example 1: Standard Comprehensive Assessment
    print("1. COMPREHENSIVE ASSESSMENT")
    print("-" * 30)

    try:
        result = example_comprehensive_assessment(
            knowledge_store,
            governance_db,
            ai_system_context
        )

        print(f"Workflow ID: {result['workflow_id']}")
        print(f"Overall Risk: {result['overall_risk']}")
        print(f"Compliance Status: {result['compliance_status']}")
        print(f"Execution Time: {result['execution_time']:.2f}s")
        print(f"Agents Used: {', '.join(result['agents_used'])}")
        print(f"Recommendations: {len(result['recommendations'])} items")

        # Show sample recommendations
        for i, rec in enumerate(result['recommendations'][:3], 1):
            print(f"  {i}. {rec}")

    except Exception as e:
        print(f"Error in comprehensive assessment: {e}")

    print("\n" + "="*60 + "\n")

    # Example 2: Rapid Screening
    print("2. RAPID SCREENING")
    print("-" * 20)

    try:
        result = example_rapid_screening(
            knowledge_store,
            governance_db,
            ai_system_context
        )

        print(f"Workflow ID: {result['workflow_id']}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Requires Full Assessment: {result['requires_full_assessment']}")
        print(f"Execution Time: {result['execution_time']:.2f}s")

    except Exception as e:
        print(f"Error in rapid screening: {e}")

    print("\n" + "="*60 + "\n")

    # Example 3: Custom Workflow
    print("3. CUSTOM WORKFLOW")
    print("-" * 18)

    try:
        result = example_custom_workflow(
            knowledge_store,
            governance_db,
            ai_system_context
        )

        print(f"Workflow ID: {result.workflow_id}")
        print(f"Status: {result.status}")
        print(f"Agents Executed: {', '.join(result.execution_metadata.get('agents_executed', []))}")
        print(f"Overall Risk: {result.aggregated_assessment.get('overall_risk_level')}")
        print(f"Compliance: {result.aggregated_assessment.get('overall_compliance')}")

    except Exception as e:
        print(f"Error in custom workflow: {e}")

    print("\n" + "="*60 + "\n")

    # Example 4: Different Pipeline Types
    print("4. DIFFERENT PIPELINE TYPES")
    print("-" * 30)

    pipeline_types = ["standard", "rapid", "compliance", "risk"]

    for pipeline_type in pipeline_types:
        try:
            orchestrator = create_governance_pipeline(
                knowledge_store,
                governance_db,
                pipeline_type
            )

            stats = orchestrator.get_orchestrator_stats()
            health = orchestrator.health_check()

            print(f"{pipeline_type.upper()} Pipeline:")
            print(f"  Agents: {', '.join(stats['registered_agents'])}")
            print(f"  Health: {'✓' if all(health['agent_health'].values()) else '✗'}")
            print(f"  Available Workflows: {len(stats['available_workflow_types'])}")

        except Exception as e:
            print(f"Error creating {pipeline_type} pipeline: {e}")

    print("\n" + "="*60 + "\n")

    # Example 5: Builder Pattern
    print("5. WORKFLOW BUILDER PATTERN")
    print("-" * 30)

    try:
        # Create orchestrator
        orchestrator = create_governance_pipeline(knowledge_store, governance_db, "standard")

        # Build custom workflow using builder pattern
        builder = WorkflowBuilder(orchestrator)

        workflow_id = (builder
                      .add_agent('risk_agent')
                      .add_agent('bias_agent')
                      .set_context(ai_system_context)
                      .build_and_execute())

        print(f"Custom Workflow Created: {workflow_id}")

        # Execute the workflow
        result = orchestrator.execute_workflow(workflow_id)

        print(f"Execution completed:")
        print(f"  Status: {result.status}")
        print(f"  Agents: {', '.join(result.execution_metadata.get('agents_executed', []))}")
        print(f"  Duration: {result.execution_metadata.get('execution_time_seconds', 0):.2f}s")

    except Exception as e:
        print(f"Error in builder pattern example: {e}")

    print("\n" + "="*60 + "\n")

    # Example 6: Monitoring Workflows
    print("6. WORKFLOW MONITORING")
    print("-" * 22)

    try:
        orchestrator = create_governance_pipeline(knowledge_store, governance_db, "standard")

        # Create multiple workflows
        workflow_ids = []
        for i in range(3):
            wf_id = orchestrator.create_workflow(
                WorkflowType.RAPID_SCREENING,
                {**ai_system_context, "system_id": f"system_{i}"}
            )
            workflow_ids.append(wf_id)

        print(f"Created {len(workflow_ids)} workflows")

        # Check status of workflows
        for wf_id in workflow_ids:
            status = orchestrator.get_workflow_status(wf_id)
            print(f"  {wf_id}: {status['status']}")

        # Execute one workflow
        result = orchestrator.execute_workflow(workflow_ids[0])
        print(f"\nExecuted {workflow_ids[0]}:")
        print(f"  Final Status: {result.status}")
        print(f"  Risk Assessment: {result.aggregated_assessment.get('overall_risk_level')}")

        # Check orchestrator statistics
        stats = orchestrator.get_orchestrator_stats()
        print(f"\nOrchestrator Stats:")
        print(f"  Active Workflows: {stats['active_workflows']}")
        print(f"  Completed Workflows: {stats['completed_workflows']}")
        print(f"  Total Workflows: {stats['total_workflows']}")

    except Exception as e:
        print(f"Error in monitoring example: {e}")

    print("\n" + "="*60)
    print("Demo completed successfully!")
    print("="*60)

if __name__ == "__main__":
    main()