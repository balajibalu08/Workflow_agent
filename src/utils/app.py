from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import shutil
import json
import asyncio
import os

from src.utils.workflow import workflow

app = FastAPI(
    title="AI Resume & Spam Analyzer",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def execute_workflow(message: str):

    result = await workflow.run(message)

    outputs = result.get_outputs()

    if len(outputs) < 2:
        raise Exception("Workflow returned insufficient outputs.")

    routing = json.loads(outputs[0].text)

    final = json.loads(outputs[-1].text)

    if "candidate" in final:
        result_type = "resume"

    elif "is_spam" in final:
        result_type = "spam"

    else:
        result_type = "unknown"

    return {
        "routing": routing,
        "result": {
            "type": result_type,
            "data": final
        }
    }

@app.get("/")
async def root():
    return {
        "message": "AI Resume & Spam Analysis API Running"
    }


@app.post("/analyze/resume")
async def analyze_resume(
        file: UploadFile = File(...)
):

    temp_dir = tempfile.mkdtemp()

    file_path = os.path.join(
        temp_dir,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    message = json.dumps({
        "user_input": "Analyze this resume.",
        "input_source": file_path
    })

    try:

        response = await execute_workflow(message)

        return response

    finally:

        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass


@app.post("/analyze/spam")
async def analyze_spam(
        email_text: str = Form(...)
):

    message = json.dumps({
        "user_input": "Analyze this email.",
        "input_source": email_text
    })

    return await execute_workflow(message)