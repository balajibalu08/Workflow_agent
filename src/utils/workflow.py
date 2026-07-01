from agent_framework import WorkflowBuilder
from src.executors.executor import DocumentExtractionExecutor
from agents.resume_analysis import ResumeAnalysisAgent
from src.utils.logs import logger

document_extraction_executor = DocumentExtractionExecutor()
logger.info("DocumentExtractionExecutor initialized successfully.")
resume_analysis_agent = ResumeAnalysisAgent()
logger.info("ResumeAnalysisAgent initialized successfully.")

workflow = WorkflowBuilder(
    name="Resume_Analysis_Workflow", 
    description="Workflow to extract text from PDF and analyze resumes.",
    start_executor=document_extraction_executor
    ).add_edge(
        document_extraction_executor, resume_analysis_agent.agent
        ).build()
logger.info("Workflow built successfully.")