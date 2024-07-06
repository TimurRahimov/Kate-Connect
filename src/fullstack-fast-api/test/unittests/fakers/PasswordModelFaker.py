from faker import Faker
from uuid import uuid4

from src.domain.models import PasswordModel

fake = Faker()


class PasswordModelFaker:

    def __init__(self, user_id: str):
        password = uuid4().hex
        self.__model = PasswordModel(
            user_id=user_id,
            password=password
        )

    @property
    def model(self):
        return self.__model
