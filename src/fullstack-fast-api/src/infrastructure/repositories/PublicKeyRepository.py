import os
import re

from src.domain.exceptions import PublicKeyNotFoundError, UserNotFoundError
from src.domain.abstractions.repositories import IPublicKeyRepository
from src.domain.models import PublicKeyModel

REPO_ABS_PATH = os.path.dirname(os.path.abspath(__file__))
ETC_PATH = os.path.join(REPO_ABS_PATH, "..", "etc")
USERS_PATH = os.path.join(ETC_PATH, "users")

USER_ID_PATTERN = r"\(\.\*\)\\"
PUBLICKEY_SAVE_PATTERN = r"public_(.*)\.key"


def make_pk_filename_from_user_id(user_id: str) -> str:
    return re.sub(USER_ID_PATTERN, user_id, PUBLICKEY_SAVE_PATTERN)


class PublicKeyRepository(IPublicKeyRepository):

    async def add(self, public_key: PublicKeyModel):
        user_folder_path = os.path.join(USERS_PATH, public_key.user_id)
        if not os.path.exists(user_folder_path):
            raise UserNotFoundError()

        pk_filename = make_pk_filename_from_user_id(public_key.user_id)
        publickey_path = os.path.join(user_folder_path, pk_filename)

        with open(publickey_path, "w") as f:
            f.write(public_key.public_key)

    async def query(self, user_id: str) -> PublicKeyModel | None:
        try:
            user_folder_path = os.path.join(USERS_PATH, user_id)
            if not os.path.exists(user_folder_path):
                raise UserNotFoundError()

            pk_filename = make_pk_filename_from_user_id(user_id)
            publickey_path = os.path.join(user_folder_path, pk_filename)

            if not os.path.exists(publickey_path):
                raise PublicKeyNotFoundError()

            with open(publickey_path, "r") as f:
                public_key = f.read()
                return PublicKeyModel(user_id=user_id, public_key=public_key)

        except (UserNotFoundError, PublicKeyNotFoundError):
            return

    async def delete(self, user_id: str) -> bool:
        pass
