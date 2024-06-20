import json
from typing import Any

from fastapi import WebSocket

from src.domain.abstractions.event_buses import IEventConsumer


class EventConsumer(IEventConsumer):

    def __init__(self, websocket: WebSocket):
        self.__ws = websocket

    async def send_obj(self, obj: Any):
        await self.send_text(json.dumps(obj))

    async def send_text(self, data: str):
        await self.__ws.send_text(data)
