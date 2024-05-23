import json
import os
from multiprocessing import Process
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from partselect.partselect.spiders.model import ModelSpider
from partselect.partselect.spiders.part_details import PartDetailsSpider
from utils.constants import openai_model, openai_temperature
from utils.helper import get_model_data, get_part_data
from utils.openai import get_openai_client
from utils.scrapper_process import ScrapperProcess
from utils.tools import tools

app = FastAPI(
    title="Server for processing partselect chat bot",
    description="""A simple partselect chat bot server""",
    version=1.0,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_client = get_openai_client()


def run_model_scrape(arg):
    scrapper_process = ScrapperProcess(ModelSpider)
    scrapper_process.start(**arg)


def run_model_wrapper(model_number: str):
    
    msg = {"model_number": model_number}
    multi_processing = Process(target=run_model_scrape, args=(msg,))
    multi_processing.start()
    multi_processing.join()  # this will block until sub-process is done

    return get_model_data(model_number)


def run_part_scrape(arg):
    scrapper_process = ScrapperProcess(PartDetailsSpider)
    scrapper_process.start(**arg)


def run_part_wrapper(partselect_number: str):
    msg = {"partselect_number": partselect_number}
    multi_processing = Process(target=run_part_scrape, args=(msg,))
    multi_processing.start()
    multi_processing.join()

    return get_part_data(partselect_number)


available_functions = {
    "get_model_details": run_model_wrapper,
    "get_part_details": run_part_wrapper,
}


class Message(BaseModel):
    role: str
    content: str


class MessageBody(BaseModel):
    messages: List[Message]


#! serching for model with brand name is causing the server to crash, have to make a better prompt to avoid calling function with brand name
def get_open_ai_response(messages: List[Dict[str, str]]):
    assistant = openai_client.beta.assistants.create(
        # instructions="You are a chat bot. You have only knowledge about partselect dishwashers and refrigerators. You can answer anything about their models, parts, what parts can be fixed or replaced. Only execute the functions when a specific model detail is asked with its model number or part details is asked with its part select number.",
        instructions="""
            You are a chatbot designed to assist users with detailed information and troubleshooting for refrigerators and dishwashers. Your expertise includes:

                1. Scraping the PartSelect website to retrieve detailed information on refrigerators and dishwashers only based on their model number. Only call the model details function with a model_number, not from name of the brand like (Whirlpool, Samsung, etc), ask specifically for the model number from the user.
                2. Comprehensive knowledge of all parts of refrigerators and dishwashers, including their functions, compatibility with different manufacturers, and where each part is located. Only call the part details function with a partselect_number, not from name of the brand, ask specifically for the partselect_number from the user.
                3. Providing expert troubleshooting advice for common and complex issues with refrigerators and dishwashers.
                When responding to users, you can:
                4. Retrieve and present specific model details and part information from the PartSelect.com website.
                5. Explain the function and placement of various parts within refrigerators and dishwashers.
                6. Advise on the compatibility of parts with different refrigerator and dishwasher models and manufacturers.
                7. Help diagnose problems based on user descriptions and suggest potential fixes.

            Remember to always provide clear, concise, and accurate information to assist the user effectively. Do not call the functions without the appropriate data. Call the model details function with only model number and part details function with partselect number. To distinguish between the partselect number and model number, the part select number always starts with "PS". If possible, always prefer to give install instructions for a part as the video link if available. Try not to repeat information that is already present unless specifically asked for.
        """,
        model=openai_model,
        tools=tools,
        temperature=openai_temperature,
        top_p=1,
    )
    thread = openai_client.beta.threads.create(messages=messages)

    run = openai_client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    if run.status == "completed":
        messages = openai_client.beta.threads.messages.list(thread_id=thread.id)

    tool_outputs = []

    if not run.required_action:
        yield messages.data[0].content[0].text.value
        return

    for tool in run.required_action.submit_tool_outputs.tool_calls:
        function_name = tool.function.name
        function_arguments = json.loads(tool.function.arguments)

        function_response = available_functions[function_name](**function_arguments)

        tool_outputs.append(
            {"tool_call_id": tool.id, "output": json.dumps(function_response)}
        )

    # Submit all tool outputs at once after collecting them in a list
    if tool_outputs:
        try:
            with openai_client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
            ) as stream:
                for text in stream.text_deltas:
                    yield text
        except Exception as e:
            print("failed to submit tool outputs:", e)
    else:
        print("no tool outputs to submit.")


@app.get("/")
async def read_root():
    return {"fastapi": "server is running, visit /docs for documentation"}


@app.get("/scrape/model/{model_number}")
def scrape_model(model_number: str):
    try:
        return run_model_wrapper(model_number)
    except:
        raise HTTPException(404, "model not found")


@app.get("/scrape/part/{partselect_number}")
def scrape_part(partselect_number: str):
    try:
        return run_part_wrapper(partselect_number)
    except:
        raise HTTPException(404, "part not found")


@app.post(
    "/chatbot/",
)
async def chatbot(body: MessageBody):
    return StreamingResponse(
        get_open_ai_response(body.messages), media_type="text/event-stream"
    )
