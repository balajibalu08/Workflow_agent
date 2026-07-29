from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    AgentInterface
)
from src.utils.logs import logger
resume_skill = AgentSkill(
    id = "resume_analysis",
    name = "Resume Analysis",
    description="A Agent which analyse the Resume  sends response to client",
    input_modes=['text/plain'],
    output_modes=['text/plain'],
    tags=['resume','a2a'],
    examples=['hi analyse my resume c/resume.pdf', 'hi analyse my resume']
)
logger.info("resume skil created")
mail_skill = AgentSkill(
    id = "mail_analysis",
    name = "Mail Analysis",
    description="A Agent which analyse the Mails and gives wheter its spam or not spam  sends response to client",
    input_modes=['text/plain'],
    output_modes=['text/plain'],
    tags=['spam','mail','a2a'],
    examples=['hi analyse my mail']
)
logger.info("Mail Skill Created")
agent_card = AgentCard(
    name = "RASAA",
    description="A Agent which analyse the Resume or Mail and sends response to client",
    version="0.0.1",
    default_input_modes=['text/plain'],
    default_output_modes=['text/plain'],
    capabilities=AgentCapabilities(streaming = True),
    supported_interfaces= [AgentInterface(
        protocol_binding='JSONRPC',
        url='http://127.0.0.1:9999',
        protocol_version='1.0',
    )],
    skills=[resume_skill,mail_skill]
)
logger.info(" Agent card created")
