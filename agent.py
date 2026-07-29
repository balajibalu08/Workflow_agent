import asyncio
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import DefaultAzureCredential
from dotenv import load_dotenv
import os
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import DefaultAzureCredential
async def main():
    agent = Agent(
        client=FoundryChatClient(
            credential=DefaultAzureCredential(),
            project_endpoint="https://a2aproject.services.ai.azure.com/api/projects/a2aproj",
            model="gpt-5.1-deployment",
        ),
        instructions="You are a helpful assistant",
    )
    response = await agent.run("Hello!")
    print(response)
if __name__ == "__main__":
    asyncio.run(main())
