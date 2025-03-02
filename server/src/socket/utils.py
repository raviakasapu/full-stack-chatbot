from  fastapi import WebSocket, status, Query
from typing import Optional

async def get_token(
        websocket: WebSocket,
        token: Optional[str] = Query(None, title="Token", description="Token to be validated")
):
    if token is None or token == "":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Token is required")

    return token