from agent_framework import AgentExecutorResponse, WorkflowBuilder
from src.agents.spam_analysis_agent import SpamAnalysisAgent
from src.models.route_decision_models import RouteDecision
from src.executors.document_extraction_executor import DocumentExtractionExecutor
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
workflow = WorkflowBuilder(
    name="Workflow_resume_email_analysis", 
    description="Workflow to extract text from PDF and analyze resumes. or analyze email content for spam detection.",
    start_executor=router_agent.agent
    #spam route
    ).add_edge(
        router_agent.agent, spam_analysis_agent.agent, condition=get_condition("spam_detection","text")
        ).add_edge(
            router_agent.agent, human_input_executor.handle_human_input, condition=get_condition("spam_detection", "missing")
        ).add_edge(
            human_input_executor.handle_human_input, router_agent.agent)

    #resume route for file input
workflow.add_edge(
    router_agent.agent, document_extraction_executor.PDF_Extractor, condition=get_condition("resume_analysis", "file")
).add_edge(
    document_extraction_executor.PDF_Extractor, resume_analysis_agent.agent)
    #resume route for url input
workflow.add_edge(
    router_agent.agent, pdf_downloader_executor.download_pdf, condition=get_condition("resume_analysis", "url")).add_edge(
    pdf_downloader_executor.download_pdf, document_extraction_executor.PDF_Extractor)
workflow.add_edge(
    router_agent.agent, human_input_executor.handle_human_input, condition=get_condition("unknown"))
workflow.build()
logger.info("Workflow built successfully.")