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
    async def handle_human_input(self, response: AgentExecutorResponse, context: WorkflowContext[str]):
        """
        This method handles human input and sends it to the next agent in the workflow.
        """
        route = RouteDecision.model_validate_json(
            response.agent_response.text
        )
        prompt = route.user_prompt
        user_input = input(f"{route.source_value}\n> ")
        await context.send_message(user_input)