import os
from datetime import datetime
from fastapi import APIRouter, Depends, FastAPI, WebSocket, Request, BackgroundTasks, HTTPException, WebSocketDisconnect
import uuid 
from uuid import UUID

#from redis.commands.json.path import Path

from src.socket.connection import ConnectionManager
from src.socket.utils import get_token

from src.redis.producer import Producer
from src.redis.config import Redis
#from src.schema.chat_schema import Chat

from pydantic import BaseModel
from typing import List

chat = APIRouter()
manager = ConnectionManager()
redis = Redis()

class Chat(BaseModel):
    id: str
    messages: List
    name: str
    session_start: str

@chat.post("/token")
async def toekn_generator(name : str, request:Request):
    
    if name == "":
        raise HTTPException(status_code=400, detail={
            "loc": "name", "msg": "Name is required"
        })
    
    token = str(uuid.uuid4())
    chat_session = Chat(
        id = token,
        messages = [],
        name = name,
        session_start = str(datetime.now())
    )

    json_client = redis.create_rejson_connection()
    # Convert the model to dict and ensure UUID is converted to string
    chat_dict = chat_session.dict()
    chat_dict['id'] = str(chat_dict['id'])  # Convert UUID to string
    
    json_client.json().set(str(token), '$', chat_dict)
    redis_client = await redis.create_connection()
    await redis_client.set(str(token), 3600)
    return chat_dict

@chat.post("refresh_token")
async def refresh_token(request:Request):
    return None

@chat.websocket("/chat")
#async def websocket_endpoint(websocket: WebSocket = WebSocket, token: str = Depends(get_token)):
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(get_token)):
    await manager.connect(websocket)
    redis_client = await redis.create_connection()
    producer = Producer(redis_client)

    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            stream_data = {}
            stream_data[token] = data
            await manager.send_personal_message(f"temporary data received from chat", websocket)
            await producer.add_to_stream(stream_data, "message_channel")
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
