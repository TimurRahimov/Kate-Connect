from uuid import uuid4

from src.domain.abstractions.event_buses import IRealTimeEventBus
from src.domain.abstractions.repositories import IMessageRepository, IEncodingRepository, IChatRepository
from src.domain.abstractions.services import IMessageService, ISessionService, IUserService, IChatService
from src.domain.entities import MessageEntity, MessageAttachmentEntity, MessageEncodingEntity
from src.domain.models import SessionModel, MessageModel, MessageType, AttachmentModel, EncodingModel
from src.utils.time import iso_time, utcnow_iso


class MessageService(IMessageService):

    def __init__(self, session_service: ISessionService,
                 user_service: IUserService,
                 chat_repo: IChatRepository,
                 chat_service: IChatService,
                 message_repo: IMessageRepository,
                 encoding_repo: IEncodingRepository,
                 realtime_eventbus: IRealTimeEventBus):
        self.__session_service = session_service
        self.__chat_repo = chat_repo
        self.__chat_service = chat_service
        self.__message_repo = message_repo
        self.__encoding_repo = encoding_repo
        self.__user_service = user_service
        self.__realtime_eventbus = realtime_eventbus

    async def __to_model(self, message_entity: MessageEntity, session: SessionModel) -> MessageModel:
        message_model = MessageModel(
            message_id=message_entity.message_id,
            from_user=(await self.__user_service.get_user(message_entity.from_id, session)),
            chat_id=message_entity.chat_id,
            chat=(await self.__chat_service.get_chat(session, message_entity.chat_id)),
            timestamp=iso_time(message_entity.timestamp),
            message_type=message_entity.message_type,
            shown_list=message_entity.shown_list,
            edited=message_entity.edited,
            encodings={
                encoding_entity.for_id: EncodingModel(
                    encoding_id=encoding_entity.encoding_id,
                    chat_id=encoding_entity.chat_id,
                    message_id=encoding_entity.message_id,
                    for_id=encoding_entity.for_id,
                    encoding=encoding_entity.encoding
                ) for encoding_entity in [
                    await self.__encoding_repo.query(message_entity.message_id, for_id) for for_id in
                    message_entity.encodings.keys()]
            },
            attachments=[
                AttachmentModel(
                    attachment_id=a_entity.attachment_id,
                    message_id=a_entity.message_id,
                    attachment_type=a_entity.attachment_type,
                    attachment_url=a_entity.attachment_url
                ) for a_entity in message_entity.attachments.values()
            ]
        )

        return message_model

    async def send_message(self, session: SessionModel, chat_id: str,
                           message_type: MessageType = MessageType.SIMPLE,
                           encodings: dict[str, str] = None,
                           attachments: list[AttachmentModel] = None) -> MessageModel | None:
        if not await self.__session_service.verify(session):
            return

        chat_entity = await self.__chat_repo.query(chat_id)

        if chat_entity is None or session.user_id not in chat_entity.members:
            return

        if encodings is None:
            encodings = {}

        if attachments is None:
            attachments = []

        message_id = uuid4().hex

        encoding_entities = [
            MessageEncodingEntity(
                chat_id=chat_id,
                encoding_id=uuid4().hex,
                message_id=message_id,
                for_id=for_id,
                encoding=encoding
            ) for for_id, encoding in encodings.items()
        ]

        for encoding_entity in encoding_entities:
            await self.__encoding_repo.add(encoding_entity)

        message_entity = MessageEntity(
            message_id=message_id,
            from_id=session.user_id,
            chat_id=chat_id,
            timestamp=utcnow_iso(),
            message_type=message_type,
            shown=False,
            edited=False,
            encodings={
                encoding.for_id: encoding.encoding_id for encoding in encoding_entities
            },
            attachments={
                a_model.attachment_id: MessageAttachmentEntity(
                    attachment_id=a_model.attachment_id,
                    message_id=a_model.message_id,
                    attachment_type=a_model.message_id,
                    attachment_url=a_model.attachment_url) for a_model in attachments
            }
        )

        await self.__message_repo.add(message_entity)

        message_model = await self.__to_model(message_entity, session)

        for member_id in chat_entity.members:
            await self.__realtime_eventbus.new_message_event(member_id, message_model)

        return message_model

    async def get_message(self, session: SessionModel,
                          chat_id: str, message_id: str) -> MessageModel | None:
        if not await self.__session_service.verify(session):
            return

        if session.user_id not in (await self.__chat_repo.query(chat_id)).members:
            return

        message_entity = await self.__message_repo.query(chat_id, message_id)
        return await self.__to_model(message_entity, session)

    async def set_attachments(self, session: SessionModel, chat_id: str, message_id: str,
                              attachments: list[AttachmentModel] = None) -> MessageModel | None:
        pass

    async def set_encoding(self, session: SessionModel, chat_id: str, message_id: str, for_id: str,
                           encoding: str) -> MessageModel | None:

        """
        Если session.user_id = MessageModel.from_id И
        Если encoding уже существует, то меняем и edited = True
        """
        if not await self.__session_service.verify(session):
            return

        if session.user_id not in (await self.__chat_repo.query(chat_id)).members:
            return

        message_entity = await self.__message_repo.query(chat_id, message_id)

        if for_id in message_entity.encodings:
            encoding_entity = await self.__encoding_repo.query(message_id, for_id)
            if encoding_entity.encoding != encoding:
                encoding_entity.encoding = encoding
                message_entity.edited = True
        else:
            encoding_entity = MessageEncodingEntity(
                chat_id=chat_id,
                encoding_id=uuid4().hex,
                message_id=message_id,
                for_id=for_id,
                encoding=encoding
            )

        message_entity.encodings[for_id] = encoding_entity.encoding_id

        await self.__message_repo.update(message_entity)
        await self.__encoding_repo.add(encoding_entity)

        return await self.__to_model(message_entity, session)

    async def set_shown(self, session: SessionModel, chat_id: str, message_id: str) -> MessageModel | None:
        if not await self.__session_service.verify(session):
            return

        if session.user_id not in (await self.__chat_repo.query(chat_id)).members:
            return

        message_entity = await self.__message_repo.query(chat_id, message_id)

        if session.user_id == message_entity.from_id:
            return

        message_entity.shown_list.append(session.user_id)
        await self.__message_repo.update(message_entity)

        return await self.__to_model(message_entity, session)

    async def query_messages(self, session: SessionModel, chat_id: str, offset: int, count: int) -> list[MessageModel]:
        return [await self.__to_model(m, session) for m in
                await self.__message_repo.query_last(chat_id=chat_id, count=count)]
#
#
#
# def __init__(self, session_service: ISessionService,
# 			 message_repo: IMessageRepository,
# 			 encoding_repo: IEncodingRepository):
# 	self.__session_service = session_service
# 	self.__message_repo = message_repo
# 	self.__encoding_repo = encoding_repo
#
# def __to_model(self, message_entity: MessageEntity) -> MessageModel:
# 	message_model = MessageModel(
# 		message_id=message_entity.message_id,
# 		from_id=message_entity.from_id,
# 		chat_id=message_entity.chat_id,
# 		timestamp=iso_time(message_entity.timestamp),
# 		message_type=message_entity.message_type,
# 		shown=message_entity.shown,
# 		edited=message_entity.edited,
# 		encodings=[
# 			EncodingModel(
# 				chat_id=encoding_entity.chat_id,
# 				message_id=encoding_entity.message_id,
# 				for_id=encoding_entity.for_id,
# 				encoding=encoding_entity.encoding
# 			) for encoding_entity in [await self.__encoding_repo.query(encoding_id) for encoding_id in message_entity.encodings.values()]
# 		],
# 		attachments=[
# 			AttachmentModel(
# 				attachment_id=a_entity.attachment_id,
# 				message_id=a_entity.message_id
# 				attachment_type=a_entity.message_id,
# 				attachment_url=a_entity.attachment_url
# 			) for a_entity in message_entity.attachments.values()
# 		]
# 	)
#
# 	return message_model
#
# async def send_message(self, session: SessionModel, chat_id: str,
# 					   message_type: MessageType = MessageType.SIMPLE,
# 					   attachments: list[AttachmentModel] = []) -> MessageModel | None:
# 	"""
# 	from_id = session.user_id
# 	encodings = []
# 	Автоматически: message_id, timestamp, shown, edited
# 	"""
# 	if not await self.__session_service.verify(session):
# 		return
#
#
# 	# Chat-user сравнить, есть ли session.user_id в данном чате
#
# 	message_id = uuid4().hex
# 	message_entity = MessageEntity(
# 		message_id=message_id,
# 		from_id=session.user_id,
# 		chat_id=chat_id,
# 		timestamp=iso_now(),
# 		message_type=message_type,
# 		shown=False,
# 		edited=False,
# 		encodings={},
# 		attachments={
# 			a_model.attachment_id : MessageAttachmentEntity(
# 				attachment_id=a_model.attachment_id,
# 				message_id=a_model.message_id
# 				attachment_type=a_model.message_id,
# 				attachment_url=a_model.attachment_url
# 			) for a_model in attachments
# 		}
# 	)
#
# 	await self.__message_repo.add(message_entity)
# 	return self.__to_model(message_entity)
#
#
# async def get_message(self, session: SessionModel, chat_id: str, message_id: str) -> MessageModel | None:
# 	if not await self.__session_service.verify(session):
# 		return
#
# 	# Chat-user сравнить, есть ли session.user_id в данном чате
#
# 	message_entity = await self.__message_repo.query(encoding.chat_id, encoding.message_id)
# 	return self.__to_model(message_entity)
#
#
#
# async def set_attachments(self, session: SessionModel, chat_id: str, message_id: str,
# 						  attachments: list[AttachmentModel] = []) -> MessageModel | None:
# 	pass
#
#
# async def set_encoding(self, session: SessionModel, chat_id: str, message_id: str, for_id: str, encoding: str) -> MessageModel | None:
# 	"""
# 	Если session.user_id = MessageModel.from_id И
# 	Если encoding уже существует, то меняем и edited = True
# 	"""
# 	if not await self.__session_service.verify(session):
# 		return
#
# 	# Chat-user сравнить, есть ли session.user_id в данном чате
#
# 	message_entity = await self.__message_repo.query(chat_id, message_id)
#
# 	if for_id in message_entity.encodings:
# 		encoding_entity = await self.__encoding_repo.query(encoding.message_id, encoding.for_id)
# 		if encoding_entity.encoding != encoding:
# 			encoding_entity.encoding = encoding
# 			message_entity.edited = True
# 	else:
# 		encoding_entity = MessageEncodingEntity(
# 			encoding_id=uuid4().hex,
# 			message_id=message_id,
# 			for_id=for_id,
# 			encoding=encoding
# 		)
#
# 	message_entity.encodings[for_id] = encoding_entity.encoding_id
#
# 	await self.__message_repo.add(message_entity)
# 	await self.__encoding_repo.add(encoding_entity)
#
# 	return self.__to_model(message_entity)
#
# async def set_shown(self, session: SessionModel, chat_id: str, message_id: str) -> MessageModel | None:
# 	"""
# 	Если session.user_id != MessageModel.from_id, добавляем session.user_id в shown_list
# 	"""
# 	pass
#
# async def query_messages(self, session: SessionModel, chat_id: str, offset: int, count: int) -> list[MessageModel]:
# 	"""
# 	offset - величина отступа от самого последнего сообщения
# 	count - количество последних сообщений
# 	"""
# 	pass
#
#
