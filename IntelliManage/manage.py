import logging
from fastapi import APIRouter, Body, FastAPI, HTTPException
from assistant import process_assistant_task
import traceback
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import traceback
from fastapi import FastAPI, Query
from typing import Dict, List
from dotenv import load_dotenv
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
import uuid
# from project_add import verify_authentication
# from tools import get_all_projects
import logging

from assistant import process_assistant_task
class Client:
    class Beta:
        class Threads:
            def create(self):
                return type("Thread", (), {"id": str(uuid.uuid4())})()

load_dotenv()
app = FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Initialize logger
logger = logging.getLogger("websocket_logger")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
client = OpenAI(
    organization=os.getenv("organization"),
    api_key=os.getenv("openai_key"),
    )
connections: Dict[str, List[WebSocket]] = {}

import traceback
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import traceback
from fastapi import FastAPI, Query, Request
from typing import Dict, List
from datetime import datetime, timedelta,timezone
from helper import verify_authentication
import json
import asyncio
from dotenv import load_dotenv
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
import uuid
# from project_add import verify_authentication
# from tools import get_all_projects
import logging

from assistant import process_assistant_task
class Client:
    class Beta:
        class Threads:
            def create(self):
                return type("Thread", (), {"id": str(uuid.uuid4())})()

load_dotenv()
app = FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Initialize logger
logger = logging.getLogger("websocket_logger")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
client = OpenAI(
    organization=os.getenv("organization"),
    api_key=os.getenv("openai_key"),
    )
connections: Dict[str, List[WebSocket]] = {}
sso = os.getenv("sso")
dynamicurls = os.getenv("dynamicurl")
crudurl = os.getenv("crudurl")


router = APIRouter()
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.post("/manage/")
async def manage(request: Request, user_query: str = Body(..., embed=True)):
    try:
        user_info, authorization_header = await verify_authentication(request)
        if not user_info:
            logging.error("Unauthorized access attempt.")
            raise HTTPException(status_code=401, detail="Unauthorized")

        result = await process_assistant_task(user_query, authorization_header)
        logging.debug(f"Process assistant task result: {result}")
        return result
    except HTTPException as e:
        logging.error(f"HTTP exception occurred: {e.detail}")
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




active_connections = {}
client_id = None
@app.websocket("/manage/")
async def websocket_endpoint(websocket: WebSocket, authorization_header: str = Query(...), thread : str = Query(...)):
    logger.info(sso)
    logger.info(dynamicurls)
    logger.info(crudurl)
    global client_id  # Declare client_id as global to modify it
    thread_id = thread
    if 'Bearer' not in authorization_header:
        authorization_header = 'Bearer '+authorization_header
    if client_id is None:
        client_id = str(uuid.uuid4())
    active_connections[client_id] = websocket
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            logging.info(f"Received data: {data}")
            user_query = str(data)

            # Process the query
            result = await process_assistant_task(user_query, authorization_header,thread_id)
            await websocket.send_json(result)

    except WebSocketDisconnect:
            logger.info(f"Connection closed by client with ID: {connection_id}")
    except Exception as e:
        logger.error(f"Connection closed with error: {e}")
        logger.error(f"An error occurred: {traceback.format_exc()}")
    finally:
        if connection_id in connections:
            try:
                del connections[connection_id]
            except:pass
            logger.info(f"Connection with ID: {connection_id} removed from connections.")
