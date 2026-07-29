from dotenv import load_dotenv,find_dotenv
import os

class Env:
    def __init__(self):
        load_dotenv(dotenv_path="src\\resource_creation\\.env", override=True)
        print(find_dotenv())
        self.MICROSOFT_FOUNDRY_ENDPOINT = os.getenv("MICROSOFT_FOUNDRY_ENDPOINT")
        self.model = os.getenv("CHAT_MODEL_DEPLOYMENT_NAME")
        self.AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
        self.location = os.getenv("location")
        self.Azure_Subscription_ID = os.getenv("Azure_Subscription_ID")
        self.MICROSOFT_FOUNDRY_RESOURCE = os.getenv("MICROSOFT_FOUNDRY_RESOURCE")
        self.CHAT_MODEL_DEPLOYMENT_NAME = os.getenv("CHAT_MODEL_DEPLOYMENT_NAME")
        self.AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.EMBEDDING_MODEL_DEPLOYMENT_NAME = os.getenv("EMBEDDING_MODEL_DEPLOYMENT_NAME")
        self.RESOURCE_GROUP_NAME = os.getenv("RESOURCE_GROUP_NAME")
        self.PROJECT_ID = os.getenv("PROJECT_ID")
        self.DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.DOCUMENT_INTELLIGENCE_KEY = os.getenv("DOCUMENT_INTELLIGENCE_KEY")
        self.AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        self.AZURE_STORAGE_URL = os.getenv("AZURE_STORAGE_URL")
        self.AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        self.AZURE_FOUNDRY_KEY = os.getenv("MICROSOFT_FOUNDRY_API_KEY")
