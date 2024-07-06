from faker import Faker
from uuid import uuid4

from src.domain.models import SessionModel

fake = Faker()


class SessionModelFaker:

    def __init__(self, user_id: str):
        session_id = uuid4().hex
        self.__model = SessionModel(
            user_id=user_id,
            session_id=session_id
        )

    @property
    def model(self):
        return self.__model
