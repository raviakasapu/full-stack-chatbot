import os

from fastapi import APIRouter, Depends, FastAPI, WebSocket, Request, BackgroundTasks, HTTPException, WebSocketDisconnect
import uuid
from redis.commands.json.path import Path

from src.socket.connection import ConnectionManager
from src.socket.utils import get_token

from src.redis.producer import Producer
from src.redis.config import Redis

chat = APIRouter()
manager = ConnectionManager()
redis = Redis()

@chat.post("/token")
async def toekn_generator(name : str, request:Request):
    
    if name == "":
        raise HTTPException(status_code=400, detail={
            "loc": "name", "msg": "Name is required"
        })
    
    token = str(uuid.uuid4())
    data = {"name": name, "token": token}

    json_client = redis.create_rejson_connection()

    chat_session = Chat(
        token = token,
        messages = [],
        name = name
    )

    json_client.jsonset(str(token), Path.rootPath(), chat_session.dict())
    return data

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
