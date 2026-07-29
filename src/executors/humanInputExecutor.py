from agent_framework import (
    AgentExecutorResponse,
    Executor,
    WorkflowContext,
    handler,
)

from src.models.route_decision_models import RouteDecision

class HumanInputExecutor(Executor):
    def __init__(self):
        super().__init__(id="human_input_executor")
    @handler
    async def handle_human_input(self, response: AgentExecutorResponse, context: WorkflowContext[RouteDecision]):
        """
        This method will give you output
        """
        route = RouteDecision.model_validate_json(
            response.agent_response.text
        )
        await context.yield_output(route)