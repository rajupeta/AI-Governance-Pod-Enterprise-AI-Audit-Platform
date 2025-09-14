#!/usr/bin/env python3
"""
Governance Orchestrator Factory
Simplified creation and configuration of governance orchestrators with pre-configured agents
"""

import logging
from typing import Dict, Any, List, Optional

from .orchestrator import GovernanceOrchestrator, WorkflowType
from .base_agent import BaseGovernanceAgent

logger = logging.getLogger(__name__)

class GovernanceAgentFactory:
    """Factory for creating standardized governance agents"""

    @staticmethod
    def create_risk_agent(knowledge_store, governance_db):
        """Create and configure risk assessment agent"""
        from .risk_agent import RiskAssessmentAgent  # Assuming this exists
        return RiskAssessmentAgent(knowledge_store, governance_db)

    @staticmethod
    def create_bias_agent(knowledge_store, governance_db):
        """Create and configure bias detection agent"""
        from .bias_agent import BiasDetectionAgent  # Assuming this exists
        return BiasDetectionAgent(knowledge_store, governance_db)

    @staticmethod
    def create_policy_agent(knowledge_store, governance_db):
        """Create and configure policy compliance agent"""
        from .policy_agent import PolicyComplianceAgent  # Assuming this exists
        return PolicyComplianceAgent(knowledge_store, governance_db)

    @staticmethod
    def create_audit_agent(knowledge_store, governance_db):
        """Create and configure audit documentation agent"""
        from .audit_agent import AuditDocumentationAgent  # Assuming this exists
        return AuditDocumentationAgent(knowledge_store, governance_db)

    @staticmethod
    def create_liability_agent(knowledge_store, governance_db):
        """Create and configure liability protection agent"""
        from .liability_protection_agent import LiabilityProtectionAgent  # Assuming this exists
        return LiabilityProtectionAgent(knowledge_store, governance_db)

class OrchestratorFactory:
    """Factory for creating pre-configured governance orchestrators"""

    @classmethod
    def create_standard_orchestrator(cls, knowledge_store, governance_db,
                                   agents_config: Optional[Dict[str, bool]] = None) -> GovernanceOrchestrator:
        """
        Create orchestrator with standard agent configuration

        Args:
            knowledge_store: Knowledge store instance
            governance_db: Governance database instance
            agents_config: Dict specifying which agents to include (default: all)
                          e.g., {'risk_agent': True, 'bias_agent': False, ...}
        """
        orchestrator = GovernanceOrchestrator(knowledge_store, governance_db)

        # Default configuration includes all agents
        default_config = {
            'risk_agent': True,
            'bias_agent': True,
            'policy_agent': True,
            'audit_agent': True,
            'liability_protection_agent': True
        }

        config = agents_config or default_config

        # Register agents based on configuration
        agent_factory = GovernanceAgentFactory()

        if config.get('risk_agent', True):
            try:
                risk_agent = agent_factory.create_risk_agent(knowledge_store, governance_db)
                orchestrator.register_agent('risk_agent', risk_agent)
            except ImportError:
                logger.warning("Risk agent not available - using mock agent")
                orchestrator.register_agent('risk_agent', cls._create_mock_agent('risk_agent', knowledge_store, governance_db))

        if config.get('bias_agent', True):
            try:
                bias_agent = agent_factory.create_bias_agent(knowledge_store, governance_db)
                orchestrator.register_agent('bias_agent', bias_agent)
            except ImportError:
                logger.warning("Bias agent not available - using mock agent")
                orchestrator.register_agent('bias_agent', cls._create_mock_agent('bias_agent', knowledge_store, governance_db))

        if config.get('policy_agent', True):
            try:
                policy_agent = agent_factory.create_policy_agent(knowledge_store, governance_db)
                orchestrator.register_agent('policy_agent', policy_agent)
            except ImportError:
                logger.warning("Policy agent not available - using mock agent")
                orchestrator.register_agent('policy_agent', cls._create_mock_agent('policy_agent', knowledge_store, governance_db))

        if config.get('audit_agent', True):
            try:
                audit_agent = agent_factory.create_audit_agent(knowledge_store, governance_db)
                orchestrator.register_agent('audit_agent', audit_agent)
            except ImportError:
                logger.warning("Audit agent not available - using mock agent")
                orchestrator.register_agent('audit_agent', cls._create_mock_agent('audit_agent', knowledge_store, governance_db))

        if config.get('liability_protection_agent', True):
            try:
                liability_agent = agent_factory.create_liability_agent(knowledge_store, governance_db)
                orchestrator.register_agent('liability_protection_agent', liability_agent)
            except ImportError:
                logger.warning("Liability protection agent not available - using mock agent")
                orchestrator.register_agent('liability_protection_agent', cls._create_mock_agent('liability_protection_agent', knowledge_store, governance_db))

        logger.info(f"Created orchestrator with {len(orchestrator.get_available_agents())} agents")
        return orchestrator

    @classmethod
    def create_rapid_orchestrator(cls, knowledge_store, governance_db) -> GovernanceOrchestrator:
        """Create orchestrator optimized for rapid screening"""
        return cls.create_standard_orchestrator(
            knowledge_store,
            governance_db,
            {'risk_agent': True, 'bias_agent': False, 'policy_agent': False,
             'audit_agent': False, 'liability_protection_agent': False}
        )

    @classmethod
    def create_compliance_orchestrator(cls, knowledge_store, governance_db) -> GovernanceOrchestrator:
        """Create orchestrator focused on compliance checking"""
        return cls.create_standard_orchestrator(
            knowledge_store,
            governance_db,
            {'risk_agent': False, 'bias_agent': False, 'policy_agent': True,
             'audit_agent': True, 'liability_protection_agent': False}
        )

    @classmethod
    def create_risk_orchestrator(cls, knowledge_store, governance_db) -> GovernanceOrchestrator:
        """Create orchestrator focused on risk assessment"""
        return cls.create_standard_orchestrator(
            knowledge_store,
            governance_db,
            {'risk_agent': True, 'bias_agent': True, 'policy_agent': False,
             'audit_agent': False, 'liability_protection_agent': True}
        )

    @classmethod
    def _create_mock_agent(cls, agent_type: str, knowledge_store, governance_db) -> BaseGovernanceAgent:
        """Create a mock agent for testing/development when actual agents aren't available"""

        class MockGovernanceAgent(BaseGovernanceAgent):
            def __init__(self, knowledge_store, governance_db, agent_type):
                # Initialize without calling super().__init__ to avoid API requirements
                self.knowledge_store = knowledge_store
                self.governance_db = governance_db
                self.agent_type = agent_type
                logger.info(f"Mock {agent_type} governance agent initialized")

            def assess_system(self, system_context: Dict[str, Any]) -> Dict[str, Any]:
                """Mock assessment method"""
                return {
                    'status': 'completed',
                    'agent_type': self.agent_type,
                    'assessment_data': {
                        'risk_level': 'medium',
                        'compliance_status': 'partial',
                        'recommendations': [f'Mock recommendation from {self.agent_type}'],
                        'confidence_score': 6
                    },
                    'mock': True
                }

            def health_check(self) -> bool:
                return True

        return MockGovernanceAgent(knowledge_store, governance_db, agent_type)

class WorkflowBuilder:
    """Builder for creating custom governance workflows"""

    def __init__(self, orchestrator: GovernanceOrchestrator):
        self.orchestrator = orchestrator
        self.custom_agents = []
        self.system_context = {}

    def add_agent(self, agent_type: str) -> 'WorkflowBuilder':
        """Add an agent to the custom workflow"""
        if agent_type in self.orchestrator.get_available_agents():
            self.custom_agents.append(agent_type)
        else:
            logger.warning(f"Agent {agent_type} not available in orchestrator")
        return self

    def set_context(self, context: Dict[str, Any]) -> 'WorkflowBuilder':
        """Set system context for the workflow"""
        self.system_context = context
        return self

    def build_and_execute(self) -> str:
        """Build and execute the custom workflow"""
        if not self.custom_agents:
            raise ValueError("No valid agents specified for workflow")

        if not self.system_context:
            raise ValueError("System context must be provided")

        workflow_id = self.orchestrator.create_workflow(
            WorkflowType.COMPREHENSIVE_ASSESSMENT,  # Default type for custom workflows
            self.system_context,
            self.custom_agents
        )

        return workflow_id

def create_governance_pipeline(knowledge_store, governance_db,
                             pipeline_type: str = "standard") -> GovernanceOrchestrator:
    """
    Convenience function to create a governance pipeline

    Args:
        knowledge_store: Knowledge store instance
        governance_db: Governance database instance
        pipeline_type: Type of pipeline ('standard', 'rapid', 'compliance', 'risk')
    """

    pipeline_creators = {
        'standard': OrchestratorFactory.create_standard_orchestrator,
        'rapid': OrchestratorFactory.create_rapid_orchestrator,
        'compliance': OrchestratorFactory.create_compliance_orchestrator,
        'risk': OrchestratorFactory.create_risk_orchestrator
    }

    if pipeline_type not in pipeline_creators:
        raise ValueError(f"Unknown pipeline type: {pipeline_type}. "
                        f"Available types: {list(pipeline_creators.keys())}")

    return pipeline_creators[pipeline_type](knowledge_store, governance_db)

# Example usage functions
def example_comprehensive_assessment(knowledge_store, governance_db, system_data: Dict[str, Any]):
    """Example: Run comprehensive governance assessment"""

    # Create orchestrator
    orchestrator = create_governance_pipeline(knowledge_store, governance_db, "standard")

    # Create and execute workflow
    workflow_id = orchestrator.create_workflow(
        WorkflowType.COMPREHENSIVE_ASSESSMENT,
        system_data
    )

    result = orchestrator.execute_workflow(workflow_id)

    return {
        'workflow_id': workflow_id,
        'overall_risk': result.aggregated_assessment.get('overall_risk_level'),
        'compliance_status': result.aggregated_assessment.get('overall_compliance'),
        'recommendations': result.aggregated_assessment.get('recommendations', []),
        'execution_time': result.execution_metadata.get('execution_time_seconds'),
        'agents_used': result.execution_metadata.get('agents_executed', [])
    }

def example_rapid_screening(knowledge_store, governance_db, system_data: Dict[str, Any]):
    """Example: Run rapid risk screening"""

    orchestrator = create_governance_pipeline(knowledge_store, governance_db, "rapid")

    workflow_id = orchestrator.create_workflow(
        WorkflowType.RAPID_SCREENING,
        system_data
    )

    result = orchestrator.execute_workflow(workflow_id)

    return {
        'workflow_id': workflow_id,
        'risk_level': result.aggregated_assessment.get('overall_risk_level'),
        'requires_full_assessment': result.aggregated_assessment.get('overall_risk_level') in ['high', 'critical'],
        'execution_time': result.execution_metadata.get('execution_time_seconds')
    }

def example_custom_workflow(knowledge_store, governance_db, system_data: Dict[str, Any]):
    """Example: Create custom workflow using builder pattern"""

    orchestrator = create_governance_pipeline(knowledge_store, governance_db, "standard")

    # Build custom workflow
    workflow_id = (WorkflowBuilder(orchestrator)
                   .add_agent('risk_agent')
                   .add_agent('bias_agent')
                   .set_context(system_data)
                   .build_and_execute())

    result = orchestrator.execute_workflow(workflow_id)

    return result