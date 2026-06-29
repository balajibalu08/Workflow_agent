import json
import asyncio

from agent_framework import AgentResponseUpdate

from src.models.resume_models import ResumeAnalysis
from src.utils.logs import logger
from src.utils.workflow import workflow
from src.utils.variable import Env


async def main():
    env = Env()
    print("Project Endpoint:", env.MICROSOFT_FOUNDRY_ENDPOINT)
    print("Model:", env.CHAT_MODEL_DEPLOYMENT_NAME)
    pdf_path = "Resume.pdf"
    print(type(workflow))
    print(workflow)

    print("Runner:", workflow._runner)
    print("Max iterations:", workflow._runner._max_iterations)
    print("Type:", type(workflow._runner._max_iterations))
    events = workflow.run(pdf_path, stream=True)

    async for event in events:

        if event.type != "output":
            continue

        if not isinstance(event.data, AgentResponseUpdate):
            continue

        try:
            resume = ResumeAnalysis.model_validate(
                json.loads(event.data.text)
            )

            print("=" * 80)
            print("Candidate")
            print("=" * 80)
            print(resume.candidate)

            print("=" * 80)
            print("Skills")
            print("=" * 80)
            print(resume.skills)

            print("=" * 80)
            print("Education")
            print("=" * 80)

            for edu in resume.education:
                print(edu)

            print("=" * 80)
            print("Experience")
            print("=" * 80)

            if resume.experience:
                for exp in resume.experience:
                    print(exp)

            print("=" * 80)
            print("Projects")
            print("=" * 80)

            if resume.projects:
                for project in resume.projects:
                    print(project)

            print("=" * 80)
            print("Certifications")
            print("=" * 80)

            if resume.certifications:
                for cert in resume.certifications:
                    print(cert)

            print("=" * 80)
            print("Achievements")
            print("=" * 80)

            if resume.achievements:
                for achievement in resume.achievements:
                    print(achievement)

            print("=" * 80)
            print("Languages")
            print("=" * 80)

            if resume.languages:
                for language in resume.languages:
                    print(language)

            print("=" * 80)
            print("AI Analysis")
            print("=" * 80)
            print(resume.ai_analysis)

        except Exception as e:
            logger.exception(e)
            print(event.data.text)


if __name__ == "__main__":
    asyncio.run(main())