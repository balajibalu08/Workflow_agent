import json

from agent_framework import AgentExecutorResponse, WorkflowBuilder
from src.agents.spam_analysis_agent import SpamAnalysisAgent
from src.models.route_decision_models import RouteDecision
from src.executors.document_extraction_executor import DocumentExtractionExecutor, PathTransformer
from src.agents.resume_analysis import ResumeAnalysisAgent
from src.utils.logs import logger
from src.agents.RouterAgent import RouterAgent
from src.executors.pdf_downloader import PDFDownloadExecutor
import asyncio
from src.executors.humanInputExecutor import HumanInputExecutor
from typing import Any
human_input_executor = HumanInputExecutor()
logger.info("HumanInputExecutor initialized successfully.")
document_extraction_executor = DocumentExtractionExecutor()
logger.info("DocumentExtractionExecutor initialized successfully.")
pdf_downloader_executor = PDFDownloadExecutor()
logger.info("PDFDownloadExecutor initialized successfully.")
resume_analysis_agent = ResumeAnalysisAgent()
logger.info("ResumeAnalysisAgent initialized successfully.")
router_agent = RouterAgent()
spam_analysis_agent = SpamAnalysisAgent()
logger.info("RouterAgent and SpamAnalysisAgent initialized successfully.")
path_transformer = PathTransformer()
logger.info("PathTransformer initialized successfully.")

def get_condition(intent: str, input_source: str | None = None):
    """
    This function takes user input and uses the RouterAgent to determine the next step in the workflow.
    It returns a string indicating which executor or agent should handle the next step.
    """
    def condition_evaluator(message: Any) -> bool:
        if not isinstance(message, AgentExecutorResponse):
            return False
        try:
            detection = RouteDecision.model_validate_json(message.agent_response.text)
            if detection.intent !=intent:
                return False
            if input_source and detection.input_source != input_source:
                return False
            return True
        except Exception as e:
            logger.error(f"Error validating RouteDecision: {e}")
            return False
        
    return condition_evaluator
def needs_human_input(ctx):
    return (
        get_condition("spam_detection", "missing")(ctx)
        or get_condition("resume_analysis", "missing")(ctx)
        or get_condition("unknown")(ctx)
    )   

workflow = WorkflowBuilder(
    name="Workflow_resume_email_analysis", 
    description="Workflow to extract text from PDF and analyze resumes. or analyze email content for spam detection.",
    start_executor=router_agent.agent
    #spam route
    ).add_edge(
        router_agent.agent, spam_analysis_agent.agent, condition=get_condition("spam_detection","text")
        )

    #resume route for file input
workflow.add_edge(
    router_agent.agent, path_transformer, condition=get_condition("resume_analysis", "file")
).add_edge(
    path_transformer, document_extraction_executor
).add_edge(
    document_extraction_executor, resume_analysis_agent.agent)
    #resume route for url input
workflow.add_edge(
    router_agent.agent, pdf_downloader_executor, condition=get_condition("resume_analysis", "url")).add_edge(
    pdf_downloader_executor, document_extraction_executor)
workflow.add_edge(
    router_agent.agent, human_input_executor, condition=needs_human_input)
workflow = workflow.build()
logger.info("Workflow built successfully.")


    


async def run_workflow(message: str):
    """
    This function runs the workflow with the given message.
    It returns the final response from the workflow.
    """
    return await workflow.run(message)


if __name__ == "__main__":
    user_input = "Please analyze my resume."
    input_source = "Resume.pdf"
    message = json.dumps({
    "user_input": user_input,
    "input_source": input_source
    })
    final_response = asyncio.run(
        run_workflow(message)
    )

    for event in final_response:
        if event.type == "output" and event.data:
            print(f"Executor: {event.executor_id}")
            print(event.data.text)