from agent_framework import (
    Executor,
    WorkflowContext,
    handler,
)

class HumanInputExecutor(Executor):
    @handler
    async def handle_human_input(self, prompt: str, context: WorkflowContext[str]):
        """
        This method handles human input and sends it to the next agent in the workflow.
        """
        user_input = input(f"{prompt}\n> ")
        await context.send_message(user_input)