from typing import Annotated
from ulid import ULID
from utils.crypto import Crypto
from datetime import datetime
from user.domain.user import User, Profile
from user.domain.repository.user_repo import IUserRepository
from fastapi import HTTPException, Depends
from dependency_injector.wiring import inject, Provide
from fastapi import Depends


class UserService:
    @inject  # 주입받은 객체를 사용한다고 명시함.
    def __init__(
        self, user_repo: IUserRepository
    ):  # 컨테이너에 등록한 user repo를 사용할 수 있게 됨., 그리고 명시하지 않아도 자동으로 등록됨.
        self.user_repo = user_repo
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(
        self, name: str, email: str, password: str, memo: str | None = None
    ):

        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e

        now = datetime.now()

        user: User = User(
            id=self.ulid.generate(),
            profile=Profile(name=name, email=email),
            password=self.crypto.encrypt(password),
            memo=None,
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)

        return user

    def update_user(
        self,
        user_id: str,
        name: str | None = None,
        password: str | None = None,
    ):

        user = self.user_repo.find_by_id(user_id)
        # 데이터가 전달되었을 때만 업데이트가 되도록 만들었다. 안 그려면 의도치않게 데이터가 삭제될 수도 있으니까.
        if name:
            user.profile.name = name
        if password:
            user.password = self.crypto.encrypt(password)
        user.updated_at = datetime.now()

        self.user_repo.update(user)

        return user

    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        users = self.user_repo.get_users(page, items_per_page)
        return users
