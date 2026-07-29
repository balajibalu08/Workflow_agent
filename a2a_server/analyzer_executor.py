from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState
from a2a.helpers.proto_helpers import new_task_from_user_message, new_text_message, get_message_text, new_text_part
from src.utils.workflow import run_workflow
from src.models.route_decision_models import RouteDecision
from src.models.mail_models import SpamAnalysis
from src.models.resume_models import ResumeAnalysis
from src.utils.logs import logger
class AnalyzerExecutor(AgentExecutor):
    async def execute(self, context:RequestContext, event_queue:EventQueue):
        logger.info("Executing AnalyserExecutor")
        if context.current_task:
            task = context.current_task
        else:
            task = new_task_from_user_message(context.message)
            logger.info("No task")
            await event_queue.enqueue_event(task)
        task_updater = TaskUpdater(
            event_queue=event_queue, task_id= task.id, context_id= task.context_id
        )
        await task_updater.update_status(
            state=TaskState.TASK_STATE_WORKING,
            message=new_text_message('processing request' )
        )
        query = get_message_text(context.message)
        if query:
            result = await run_workflow(query)
            for event in result:
                if event.type == "output":
                    workflow_output = event.data
                    logger.info(type(workflow_output))
                    logger.info(workflow_output)
                    if isinstance(workflow_output, RouteDecision):
                        state = TaskState.TASK_STATE_INPUT_REQUIRED
                        message = new_text_message(workflow_output.user_prompt)
                    else:
                        if isinstance(workflow_output, SpamAnalysis):
                            workflow_output = workflow_output.model_dump_json()
                        elif isinstance(workflow_output, ResumeAnalysis):
                            workflow_output = workflow_output.model_dump_json()
                        await task_updater.add_artifact(parts=[new_text_part(text=workflow_output,media_type='application/json')])
                        state = TaskState.TASK_STATE_COMPLETED
                        message = new_text_message(workflow_output)
                    await task_updater.update_status(
                        state=state,
                        message=message
                    )
        else:
            result = 'No text input is provided'
            await task_updater.update_status(
                state=TaskState.TASK_STATE_INPUT_REQUIRED,
                message=new_text_message('Please provide your request!'),
            )
        return
    async def cancel(self, context, event_queue):
        return await super().cancel(context, event_queue)()
