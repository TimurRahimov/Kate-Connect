from faker import Faker

from src.domain.models import PublicKeyModel

fake = Faker()


class PublicKeyModelFaker:

    def __init__(self, user_id: str):
        self.__model = PublicKeyModel(user_id, fake.sha256() * 5)

    @property
    def model(self):
        return self.__model
