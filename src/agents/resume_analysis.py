
import asyncio
from dotenv import load_dotenv
from agent_framework.foundry import FoundryChatClient
from src.utils.variable import Env
from src.models.resume_models import ResumeAnalysis
from src.utils.llm_prompts import ResumeAnalysisPrompt
from src.utils.logs import logger
from azure.identity import AzureCliCredential

class ResumeAnalysisAgent:
    def __init__(self):
        env = Env()
        self.endpoint = env.MICROSOFT_FOUNDRY_ENDPOINT
        self.model = env.CHAT_MODEL_DEPLOYMENT_NAME
        self.api_key = env.AZURE_FOUNDRY_KEY
        
        if not self.endpoint or not self.model or not self.api_key:
            raise ValueError("Endpoint, Model, or API Key is missing from the environment.")
            
        # The crucial fix is right here: api_version must be included
        self.client = FoundryChatClient(
            project_endpoint=self.endpoint,
            model=self.model,
            credential=AzureCliCredential(),
        )
        logger.info("OpenAIChatClient initialized successfully with Azure routing.")
        
        self.resume_analyser_agent = self.client.as_agent(
            name="Resume_Analyser",
            description="Analyzes resumes and provides insights based on the content of the resume.",
            instructions=ResumeAnalysisPrompt,
            default_options={"response_format": ResumeAnalysis},
        )
        logger.info("Resume_Analyser initialized successfully.")

    @property
    def agent(self):
        return self.resume_analyser_agent

async def main():
    agent = ResumeAnalysisAgent()
    logger.info("ResumeAnalysisAgent initialized successfully.")
    
    # Run WITHOUT stream=True
    response = await agent.agent.run(
        "Please analyze the attached resume and provide insights on the candidate's skills, experience, and suitability for the role."
    )
    
    # response.value will be your fully populated ResumeAnalysis Pydantic object!
    if response.value:
        print("\n--- RESUME ANALYSIS COMPLETE ---")
        print(response.value.model_dump_json(indent=2)) 

if __name__ == "__main__":
    asyncio.run(main())