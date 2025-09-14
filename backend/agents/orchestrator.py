#!/usr/bin/env python3
"""
AI Governance Orchestrator
Coordinates multiple specialized governance agents to provide comprehensive AI system assessments
"""

import asyncio
import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum

from .base_agent import BaseGovernanceAgent

logger = logging.getLogger(__name__)

class WorkflowType(Enum):
    """Types of governance workflows available"""
    COMPREHENSIVE_ASSESSMENT = "comprehensive_assessment"
    RISK_FOCUSED = "risk_focused"
    COMPLIANCE_CHECK = "compliance_check"
    BIAS_AUDIT = "bias_audit"
    RAPID_SCREENING = "rapid_screening"

class AgentPriority(Enum):
    """Priority levels for agent execution"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class AgentTask:
    """Represents a task to be executed by an agent"""
    agent_type: str
    priority: AgentPriority
    input_data: Dict[str, Any]
    depends_on: List[str] = None  # List of agent types this task depends on
    timeout: int = 300  # Timeout in seconds
    retry_count: int = 0
    max_retries: int = 2

@dataclass
class WorkflowResult:
    """Result from executing a governance workflow"""
    workflow_id: str
    workflow_type: WorkflowType
    status: str
    start_time: datetime
    end_time: datetime
    agent_results: Dict[str, Any]
    aggregated_assessment: Dict[str, Any]
    execution_metadata: Dict[str, Any]

class GovernanceOrchestrator:
    """
    Orchestrates multiple AI governance agents to provide comprehensive system assessments
    """

    def __init__(self, knowledge_store, governance_db):
        """Initialize the orchestrator with required dependencies"""
        self.knowledge_store = knowledge_store
        self.governance_db = governance_db
        self.agents = {}
        self.active_workflows = {}
        self.workflow_history = []

        # Threading configuration
        self.max_workers = 5
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)

        logger.info("Governance orchestrator initialized")

    def register_agent(self, agent_type: str, agent_instance: BaseGovernanceAgent):
        """Register an agent with the orchestrator"""
        if not isinstance(agent_instance, BaseGovernanceAgent):
            raise ValueError(f"Agent must inherit from BaseGovernanceAgent")

        self.agents[agent_type] = agent_instance
        logger.info(f"Registered {agent_type} agent")

    def get_available_agents(self) -> List[str]:
        """Get list of available agent types"""
        return list(self.agents.keys())

    def create_workflow(self, workflow_type: WorkflowType, system_context: Dict[str, Any],
                       custom_agents: List[str] = None) -> str:
        """Create a new governance workflow"""
        workflow_id = self._generate_workflow_id()

        # Define agent tasks based on workflow type
        tasks = self._create_workflow_tasks(workflow_type, system_context, custom_agents)

        workflow = {
            'id': workflow_id,
            'type': workflow_type,
            'system_context': system_context,
            'tasks': tasks,
            'status': 'created',
            'created_at': datetime.now(),
            'results': {},
            'metadata': {
                'total_tasks': len(tasks),
                'completed_tasks': 0,
                'failed_tasks': 0
            }
        }

        self.active_workflows[workflow_id] = workflow
        logger.info(f"Created workflow {workflow_id} with {len(tasks)} tasks")

        return workflow_id

    def execute_workflow(self, workflow_id: str) -> WorkflowResult:
        """Execute a governance workflow"""
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow {workflow_id} not found")

        workflow = self.active_workflows[workflow_id]
        workflow['status'] = 'running'
        workflow['started_at'] = datetime.now()

        try:
            # Execute tasks based on dependencies and priorities
            execution_plan = self._create_execution_plan(workflow['tasks'])
            results = self._execute_tasks(execution_plan, workflow['system_context'])

            # Aggregate results
            aggregated_assessment = self._aggregate_results(results, workflow['type'])

            # Create final result
            end_time = datetime.now()
            workflow_result = WorkflowResult(
                workflow_id=workflow_id,
                workflow_type=workflow['type'],
                status='completed',
                start_time=workflow['started_at'],
                end_time=end_time,
                agent_results=results,
                aggregated_assessment=aggregated_assessment,
                execution_metadata={
                    'execution_time_seconds': (end_time - workflow['started_at']).total_seconds(),
                    'agents_executed': list(results.keys()),
                    'total_agents': len(workflow['tasks'])
                }
            )

            # Clean up and store
            workflow['status'] = 'completed'
            workflow['completed_at'] = end_time
            self.workflow_history.append(workflow_result)
            del self.active_workflows[workflow_id]

            # Log to audit trail
            self._log_workflow_completion(workflow_result)

            return workflow_result

        except Exception as e:
            workflow['status'] = 'failed'
            workflow['error'] = str(e)
            logger.error(f"Workflow {workflow_id} failed: {str(e)}")
            raise

    def _create_workflow_tasks(self, workflow_type: WorkflowType,
                              system_context: Dict[str, Any],
                              custom_agents: List[str] = None) -> List[AgentTask]:
        """Create tasks based on workflow type"""
        tasks = []

        if custom_agents:
            # Use custom agent list
            for agent_type in custom_agents:
                if agent_type in self.agents:
                    tasks.append(AgentTask(
                        agent_type=agent_type,
                        priority=AgentPriority.HIGH,
                        input_data=system_context
                    ))
        else:
            # Use predefined workflows
            if workflow_type == WorkflowType.COMPREHENSIVE_ASSESSMENT:
                tasks = [
                    AgentTask("risk_agent", AgentPriority.CRITICAL, system_context),
                    AgentTask("bias_agent", AgentPriority.HIGH, system_context, ["risk_agent"]),
                    AgentTask("policy_agent", AgentPriority.HIGH, system_context, ["risk_agent"]),
                    AgentTask("audit_agent", AgentPriority.MEDIUM, system_context, ["risk_agent", "bias_agent", "policy_agent"]),
                    AgentTask("liability_protection_agent", AgentPriority.LOW, system_context, ["audit_agent"])
                ]

            elif workflow_type == WorkflowType.RISK_FOCUSED:
                tasks = [
                    AgentTask("risk_agent", AgentPriority.CRITICAL, system_context),
                    AgentTask("liability_protection_agent", AgentPriority.HIGH, system_context, ["risk_agent"])
                ]

            elif workflow_type == WorkflowType.COMPLIANCE_CHECK:
                tasks = [
                    AgentTask("policy_agent", AgentPriority.CRITICAL, system_context),
                    AgentTask("audit_agent", AgentPriority.HIGH, system_context, ["policy_agent"])
                ]

            elif workflow_type == WorkflowType.BIAS_AUDIT:
                tasks = [
                    AgentTask("bias_agent", AgentPriority.CRITICAL, system_context),
                    AgentTask("audit_agent", AgentPriority.HIGH, system_context, ["bias_agent"])
                ]

            elif workflow_type == WorkflowType.RAPID_SCREENING:
                tasks = [
                    AgentTask("risk_agent", AgentPriority.CRITICAL, system_context)
                ]

        return [task for task in tasks if task.agent_type in self.agents]

    def _create_execution_plan(self, tasks: List[AgentTask]) -> List[List[AgentTask]]:
        """Create execution plan respecting dependencies and priorities"""
        # Group tasks by dependency levels
        execution_levels = []
        remaining_tasks = tasks.copy()
        completed_agents = set()

        while remaining_tasks:
            current_level = []

            # Find tasks that can run now (no unfulfilled dependencies)
            for task in remaining_tasks[:]:
                if not task.depends_on or all(dep in completed_agents for dep in task.depends_on):
                    current_level.append(task)
                    remaining_tasks.remove(task)

            if not current_level:
                # Circular dependency or invalid dependency
                logger.warning("Detected circular or invalid dependencies, breaking")
                current_level = remaining_tasks
                remaining_tasks = []

            # Sort current level by priority
            current_level.sort(key=lambda x: x.priority.value)
            execution_levels.append(current_level)

            # Add completed agents
            completed_agents.update(task.agent_type for task in current_level)

        return execution_levels

    def _execute_tasks(self, execution_plan: List[List[AgentTask]],
                      system_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tasks according to the execution plan"""
        results = {}

        for level_index, level_tasks in enumerate(execution_plan):
            logger.info(f"Executing level {level_index + 1} with {len(level_tasks)} tasks")

            # Execute tasks in parallel within each level
            if len(level_tasks) == 1:
                # Single task - execute directly
                task = level_tasks[0]
                result = self._execute_single_task(task, results)
                results[task.agent_type] = result
            else:
                # Multiple tasks - execute in parallel
                level_results = self._execute_parallel_tasks(level_tasks, results)
                results.update(level_results)

        return results

    def _execute_single_task(self, task: AgentTask, previous_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single agent task"""
        agent = self.agents[task.agent_type]

        # Prepare input data with previous results if dependencies exist
        input_data = task.input_data.copy()
        if task.depends_on:
            input_data['previous_results'] = {
                dep: previous_results.get(dep) for dep in task.depends_on
            }

        try:
            # Execute agent assessment (this would be agent-specific)
            result = self._call_agent_assessment(agent, input_data)
            logger.info(f"Completed task for {task.agent_type}")
            return result

        except Exception as e:
            logger.error(f"Task failed for {task.agent_type}: {str(e)}")
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                logger.info(f"Retrying {task.agent_type} (attempt {task.retry_count})")
                return self._execute_single_task(task, previous_results)
            else:
                return {
                    'status': 'failed',
                    'error': str(e),
                    'agent_type': task.agent_type
                }

    def _execute_parallel_tasks(self, tasks: List[AgentTask],
                               previous_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute multiple tasks in parallel"""
        futures = {}
        results = {}

        # Submit all tasks
        for task in tasks:
            future = self.executor.submit(self._execute_single_task, task, previous_results)
            futures[future] = task.agent_type

        # Collect results as they complete
        for future in as_completed(futures, timeout=max(task.timeout for task in tasks)):
            agent_type = futures[future]
            try:
                result = future.result()
                results[agent_type] = result
            except Exception as e:
                logger.error(f"Parallel task failed for {agent_type}: {str(e)}")
                results[agent_type] = {
                    'status': 'failed',
                    'error': str(e),
                    'agent_type': agent_type
                }

        return results

    def _call_agent_assessment(self, agent: BaseGovernanceAgent,
                              input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Call agent assessment method - this is a placeholder for agent-specific methods"""
        # This would be implemented based on the specific agent interface
        # For now, return a mock response
        return {
            'status': 'completed',
            'agent_type': agent.agent_type,
            'assessment_data': {
                'risk_level': 'medium',
                'compliance_status': 'partial',
                'recommendations': ['Implement additional safeguards'],
                'confidence_score': 8
            },
            'execution_time': 1.5
        }

    def _aggregate_results(self, agent_results: Dict[str, Any],
                          workflow_type: WorkflowType) -> Dict[str, Any]:
        """Aggregate results from multiple agents into a comprehensive assessment"""
        successful_results = {k: v for k, v in agent_results.items()
                            if v.get('status') == 'completed'}

        if not successful_results:
            return {
                'overall_status': 'failed',
                'message': 'No agents completed successfully'
            }

        # Aggregate risk levels
        risk_levels = []
        confidence_scores = []
        all_recommendations = []
        compliance_statuses = []

        for agent_type, result in successful_results.items():
            assessment = result.get('assessment_data', {})

            if 'risk_level' in assessment:
                risk_levels.append(assessment['risk_level'])
            if 'confidence_score' in assessment:
                confidence_scores.append(assessment['confidence_score'])
            if 'recommendations' in assessment:
                all_recommendations.extend(assessment['recommendations'])
            if 'compliance_status' in assessment:
                compliance_statuses.append(assessment['compliance_status'])

        # Calculate overall risk level
        risk_priority = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        overall_risk = 'low'
        if risk_levels:
            highest_risk = max(risk_levels, key=lambda x: risk_priority.get(x, 0))
            overall_risk = highest_risk

        # Calculate average confidence
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0

        # Determine overall compliance
        overall_compliance = 'unknown'
        if compliance_statuses:
            if 'non_compliant' in compliance_statuses:
                overall_compliance = 'non_compliant'
            elif 'partial' in compliance_statuses:
                overall_compliance = 'partial'
            elif all(status == 'compliant' for status in compliance_statuses):
                overall_compliance = 'compliant'

        return {
            'overall_status': 'completed',
            'overall_risk_level': overall_risk,
            'overall_compliance': overall_compliance,
            'confidence_score': round(avg_confidence, 2),
            'total_recommendations': len(set(all_recommendations)),
            'recommendations': list(set(all_recommendations)),
            'agents_consulted': list(successful_results.keys()),
            'failed_agents': [k for k, v in agent_results.items() if v.get('status') != 'completed'],
            'workflow_type': workflow_type.value,
            'assessment_summary': self._generate_assessment_summary(successful_results)
        }

    def _generate_assessment_summary(self, results: Dict[str, Any]) -> str:
        """Generate a human-readable assessment summary"""
        agent_count = len(results)
        risk_levels = [r.get('assessment_data', {}).get('risk_level') for r in results.values()]
        risk_levels = [r for r in risk_levels if r]

        if not risk_levels:
            return f"Assessment completed with {agent_count} agents. Detailed analysis required."

        risk_counts = {level: risk_levels.count(level) for level in set(risk_levels)}
        summary = f"Multi-agent assessment completed ({agent_count} agents). "

        if risk_counts:
            risk_summary = ", ".join([f"{count} {level}" for level, count in risk_counts.items()])
            summary += f"Risk distribution: {risk_summary}."

        return summary

    def _generate_workflow_id(self) -> str:
        """Generate unique workflow ID"""
        timestamp = int(datetime.now().timestamp())
        return f"workflow_{timestamp}_{len(self.active_workflows)}"

    def _log_workflow_completion(self, result: WorkflowResult):
        """Log workflow completion to audit trail"""
        try:
            log_data = {
                'workflow_id': result.workflow_id,
                'workflow_type': result.workflow_type.value,
                'execution_time': result.execution_metadata.get('execution_time_seconds'),
                'agents_used': result.execution_metadata.get('agents_executed'),
                'overall_risk': result.aggregated_assessment.get('overall_risk_level'),
                'overall_compliance': result.aggregated_assessment.get('overall_compliance')
            }

            self.governance_db.log_audit_event(
                system_id='orchestrator',
                action='workflow_completed',
                details=json.dumps(log_data)
            )

        except Exception as e:
            logger.error(f"Failed to log workflow completion: {str(e)}")

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status of a workflow"""
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
            return {
                'id': workflow_id,
                'status': workflow['status'],
                'progress': workflow['metadata'],
                'created_at': workflow['created_at'].isoformat()
            }

        # Check completed workflows
        for result in self.workflow_history:
            if result.workflow_id == workflow_id:
                return {
                    'id': workflow_id,
                    'status': result.status,
                    'completed_at': result.end_time.isoformat(),
                    'execution_time': result.execution_metadata.get('execution_time_seconds')
                }

        return {'error': 'Workflow not found'}

    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel an active workflow"""
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id]['status'] = 'cancelled'
            del self.active_workflows[workflow_id]
            logger.info(f"Cancelled workflow {workflow_id}")
            return True
        return False

    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            'registered_agents': list(self.agents.keys()),
            'active_workflows': len(self.active_workflows),
            'completed_workflows': len(self.workflow_history),
            'total_workflows': len(self.active_workflows) + len(self.workflow_history),
            'available_workflow_types': [wf.value for wf in WorkflowType],
            'max_workers': self.max_workers
        }

    def health_check(self) -> Dict[str, Any]:
        """Check health of orchestrator and all agents"""
        agent_health = {}
        for agent_type, agent in self.agents.items():
            try:
                agent_health[agent_type] = agent.health_check()
            except Exception as e:
                agent_health[agent_type] = False
                logger.error(f"Health check failed for {agent_type}: {str(e)}")

        return {
            'orchestrator_status': 'healthy',
            'agent_health': agent_health,
            'healthy_agents': sum(1 for status in agent_health.values() if status),
            'total_agents': len(agent_health),
            'active_workflows': len(self.active_workflows)
        }