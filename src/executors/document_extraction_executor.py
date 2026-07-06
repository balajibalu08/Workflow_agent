import json
import asyncio
from agent_framework import (
    Executor,
    WorkflowContext,
    handler,
)
from dotenv import load_dotenv
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from src.models.route_decision_models import RouteDecision
from src.utils.logs import logger
from src.utils.variable import Env
from agent_framework import AgentExecutorResponse


load_dotenv(override=True)

class DocumentExtractionExecutor(Executor):
    def __init__(self):
        super().__init__(id="document_extractor")
        env = Env()
        endpoint = env.DOCUMENT_INTELLIGENCE_ENDPOINT
        key = env.DOCUMENT_INTELLIGENCE_KEY

        if not endpoint or not key:
            raise ValueError(
                "DOCUMENT_INTELLIGENCE_ENDPOINT or DOCUMENT_INTELLIGENCE_KEY is missing."
            )

        self.client = DocumentIntelligenceClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )   
    
    @handler
    async def PDF_Extractor(self, path: str, context: WorkflowContext) -> None:
        if not self.client:
            await context.send_message(json.dumps({"error": "Document Analysis client not initialized"}))
            return
        if not os.path.exists(path):
            await context.send_message(
                json.dumps({"error": f"File not found: {path}"})
            )
            return
        try:
     
            with open(path, "rb") as f:
                poller = self.client.begin_analyze_document("prebuilt-layout", body=f)
                result = poller.result()
                logger.info(f"Successfully extracted text from PDF: {path}")
            output = {
                "content": result.content,
                "key_value_pairs": {},
                "tables": [],
                "paragraphs": []
                }
            if result.key_value_pairs:
                for kvp in result.key_value_pairs:
                    k = kvp.key.content if kvp.key else "UNKNOWN_KEY"
                    v = kvp.value.content if kvp.value else "UNASSIGNED_VALUE"
                    output["key_value_pairs"][k] = v
                    
            if result.tables:
                for table in result.tables:
                    table_data = []
                    for cell in table.cells:
                        table_data.append({
                            "row": cell.row_index,
                            "col": cell.column_index,
                            "content": cell.content,
                            "type": "Header" if cell.kind in ["columnHeader", "rowHeader"] else "Data"
                        })
                    output["tables"].append(table_data)
            if result.paragraphs:
                output["paragraphs"] = [
                    paragraph.content
                    for paragraph in result.paragraphs
                ]
            
            logger.info("Successfully extracted resume text.")
            logger.info(f"Pages: {len(result.pages)}")
            logger.info(f"Characters extracted: {len(result.content)}")
            # 5. Forward the JSON payload to the next executor in the graph
            logger.info("Forwarding extracted resume to Resume Analysis Agent.")
            await context.send_message(json.dumps(output))
        except Exception as e:
            logger.exception(f"Error occurred while extracting text from PDF: {e}")
            # Include the string representation of the actual error (str(e))
            await context.send_message(json.dumps({
                "error": "Failed to extract text from PDF",
                "details": str(e)
            }))

class MockWorkflowContext:
    """
    A lightweight mock context to catch the output of the executor 
    without needing a full agent framework environment.
    """
    async def send_message(self, message: str) -> None:
        print("\n" + "="*50)
        print("✅ Message intercepted by Mock Context:")
        print("="*50)
        
        # Prettify the JSON output for easier reading in the terminal
        try:
            parsed_json = json.loads(message)
            print(json.dumps(parsed_json, indent=2))
        except json.JSONDecodeError:
            print(message)
        print("="*50 + "\n")

class PathTransformer(Executor):
    def __init__(self):
        super().__init__(id="path_transformer")
    @handler
    async def filePathTransformer(self, response: AgentExecutorResponse, context: WorkflowContext) -> None:
        logger.info("Transforming route decision to file path...")
        route: RouteDecision = RouteDecision.model_validate_json(response.agent_response.text)
        if not route.source_value:
            logger.error("RouteDecision does not contain a source_value.")
            raise ValueError("RouteDecision does not contain a source_value.")
        logger.info(f"RouteDecision received: intent={route.intent}, input_source={route.input_source}, source_value={route.source_value}")
        if route.input_source != "file":
            logger.error(f"Expected 'file', got '{route.input_source}'.")
            raise ValueError(
               
                f"Expected 'file', got '{route.input_source}'."
            )
        if route.input_source not in ("file", "url"):
            logger.error(f"Expected file or url input, got '{route.input_source}'.")
            raise ValueError(
                f"Expected file or url input, got '{route.input_source}'."
            )
        logger.info(f"Extracting file path from route decision: {route.source_value}")

        await context.send_message(route.source_value)
async def main():
    # 1. Define the path to a test PDF (update this to point to a real file)
    test_pdf_path = "Resume.pdf" 
    
    # Ensure the dummy file actually exists before we waste an API call
    if not os.path.exists(test_pdf_path):
        print(f"⚠️ Error: Please place a dummy PDF named '{test_pdf_path}' in the same directory, or update the 'test_pdf_path' variable.")
        return

    try:
        print("Initializing DocumentExtractionExecutor...")
        extractor = DocumentExtractionExecutor()
        mock_context = MockWorkflowContext()

        print(f"Running extraction on: {test_pdf_path}")
        print("Waiting for Azure Document Intelligence (this may take a few seconds)...")
        
        # 2. Call the handler directly with our mock context
        await extractor.PDF_Extractor(test_pdf_path, mock_context)
        
    except Exception as e:
        print(f"❌ Initialization or Execution failed: {e}")

if __name__ == "__main__":
    # 3. Run the async main loop
    asyncio.run(main())