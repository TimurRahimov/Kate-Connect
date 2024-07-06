from uuid import uuid4

from src.domain.abstractions.repositories import ISessionRepository, IUserRepository
from src.domain.abstractions.services import ISessionService
from src.domain.entities import UserEntity, SessionEntity, SessionEntityContainer
from src.domain.models import SessionModel
from src.utils.time import utcnow_iso, iso_time


class SessionService(ISessionService):

    def __init__(self, user_repo: IUserRepository,
                 session_repo: ISessionRepository):
        self.__user_repo = user_repo
        self.__session_repo = session_repo

    async def create_session(self, user_id: str) -> SessionModel | None:
        session_id = uuid4().hex
        utcnow = utcnow_iso()
        session_entity = SessionEntity(
            user_id=user_id,
            session_id=session_id,
            last_activity=utcnow)
        sessions_container = await self.__session_repo.query(user_id)
        if sessions_container is None:
            sessions_container = SessionEntityContainer(user_id=user_id, sessions={})
        sessions_container.sessions[session_id] = session_entity
        await self.__session_repo.add(sessions_container)

        return SessionModel(
            user_id=user_id,
            session_id=session_id,
            last_activity=iso_time(utcnow),
            confirmed=True
        )

    async def delete_session(self, session: SessionModel) -> bool:
        sessions_container = await self.__session_repo.query(session.user_id)
        if session.session_id not in sessions_container.sessions:
            return False
        del sessions_container.sessions[session.session_id]
        await self.__session_repo.add(sessions_container)
        return True

    async def get_sessions(self, user_id: str) -> list[SessionModel] | None:
        pass

    async def verify(self, session: SessionModel) -> SessionModel:
        if session.confirmed:
            return session.set_last_activity(iso_time(utcnow_iso()))

        sessions_container = await self.__session_repo.query(session.user_id)
        if sessions_container is not None:
            for user_session in sessions_container.sessions.values():
                if session.session_id == user_session.session_id:
                    utcnow = utcnow_iso()
                    user_session.last_activity = utcnow
                    session = session.confirm().set_last_activity(iso_time(utcnow))
                    await self.__session_repo.add(sessions_container)

        return session
