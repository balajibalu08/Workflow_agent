import asyncio

from src.utils.variable import Env
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from src.utils.logs import logger
from src.utils.llm_prompts import SpamAnalysisPrompt
from src.models.mail_models import SpamAnalysis

class SpamAnalysisAgent:
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
        self.spam_analysis_agent = self.client.as_agent(
            name="Spam_Analysis_Agent",
            description="Analys the email and gives output as 'spam_analysis' model",
            instructions=SpamAnalysisPrompt,
            default_options={
                "response_format" : SpamAnalysis
            }
        )
        logger.info("Spam Analysis agent is created")
    @property
    def agent(self) :
        return self.spam_analysis_agent