from faker import Faker
from uuid import uuid4

from src.domain.models import SessionModel, UserModel
from src.utils.time import utcnow_iso, iso_time

fake = Faker()


class UserV1ModelFaker:

    def __init__(self):
        user_id = uuid4().hex
        utcnow = utcnow_iso()
        self.__model = UserModel(
            nickname=fake.name(),
            user_id=user_id,
            last_time_online=iso_time(utcnow),
            session=SessionModel(
                user_id=user_id,
                session_id=uuid4().hex,
                last_activity=iso_time(utcnow),
            ),
            avatar_link=fake.image_url(),

        )

    @property
    def model(self):
        return self.__model
