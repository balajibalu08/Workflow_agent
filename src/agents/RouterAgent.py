import asyncio

from src.utils.variable import Env
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from src.utils.logs import logger
from src.utils.llm_prompts import RouterAgentPrompt
from src.models.route_decision_models import RouteDecision

class RouterAgent:
    def __init__(self):
        env = Env()
        self.endpoint = env.MICROSOFT_FOUNDRY_ENDPOINT
        self.model = env.CHAT_MODEL_DEPLOYMENT_NAME
        if not self.endpoint or not self.model:
            logger.warning(f"Missing project endpoint or model {self.endpoint} or {self.model}")
            raise ValueError("Foundry Endpoint or model cant be None or Empty")
        self.client = FoundryChatClient(
            credential= AzureCliCredential(),
            project_endpoint = self.endpoint,
            model= self.model
        )
        logger.info("Foundry Client is initialized")

        self.router_agent = self.client.as_agent(
            name="Router_Agent",
            description= "Analyzes the user's request, determines the intent, identifies the input source, and returns a RouteDecision object.",
            instructions= RouterAgentPrompt,
            default_options={
                "response_format": RouteDecision, 
            }

        )
        logger.info("Route agent created")
    async def route_request(self, user_input: str):
        response = await self.router_agent.run(user_input)
        return response.value
    @property
    def agent(self):
        return self.router_agent
    
async def main():
    agent = RouterAgent()
    logger.info("RouterAgent initialized successfully.")
    
    # Run WITHOUT stream=True
    response = await agent.agent.run(
        "Please analyze the attached resume and provide insights on the candidate's skills, experience, and suitability for the role."
    )
    
    # response.value will be your fully populated ResumeAnalysis Pydantic object!
    if response.value:
        print("\n--- RouterAgent ANALYSIS COMPLETE ---")
        print(response.value.model_dump_json(indent=2)) 

if __name__ == "__main__":
    asyncio.run(main())