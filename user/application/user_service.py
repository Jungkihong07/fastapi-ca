from ulid import ULID
from utils.crypto import Crypto
from datetime import datetime
from user.domain.user import User, Profile
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository
from fastapi import HTTPException


class UserService:
    def __init__(self):
        self.user_repo: IUserRepository = (
            UserRepository()
        )  # 해당 코드에서 의존성이 역전되어 있다.
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(self, name: str, email: str, password: str):
        _user = None

        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e

        now = datetime.now()

        user: User = User(
            id=self.ulid.generate(),
            profile=Profile(name=name,email=email),
            password=self.crypto.encrypt(password),
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)

        return user
