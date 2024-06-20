from src.domain.abstractions.event_buses import IRealTimeEventBus, IEventConsumer
from src.domain.models import MessageModel
from src.domain.models.realtime_events import RealTimeEventModel, RealTimeEventType, MessageEventModel


class RealTimeEventBus(IRealTimeEventBus):

    def __init__(self):
        self.ws_connections: dict[str, IEventConsumer] = {}

    async def connect(self, connection_id: str, consumer: IEventConsumer):
        self.ws_connections[connection_id] = consumer

    async def disconnect(self, connection_id: str):
        if connection_id in self.ws_connections:
            del self.ws_connections[connection_id]

    async def new_message_event(self, connection_id: str, message_model: MessageModel):
        if connection_id in self.ws_connections:
            event_model = RealTimeEventModel(
                RealTimeEventType.NEW_MESSAGE,
                MessageEventModel(
                    message_id=message_model.message_id,
                    from_user=message_model.from_user,
                    chat=message_model.chat,
                    timestamp=message_model.timestamp,
                    encoding=message_model.encodings[connection_id].encoding,
                    message_type=message_model.message_type,
                    attachments=message_model.attachments
                )
            )
            await self.ws_connections[connection_id].send_obj(event_model.to_dict())
