from typing import Annotated
from ulid import ULID
from common.auth import create_access_token, Role
from user.application.email_service import EmailService
from user.application.send_welcome_email_task import SendWelcomeEmailTask
from utils.crypto import Crypto
from datetime import datetime
from user.domain.user import User, Profile
from user.domain.repository.user_repo import IUserRepository
from fastapi import HTTPException, Depends, status, BackgroundTasks
from dependency_injector.wiring import inject, Provide


class UserService:
    @inject  # 주입받은 객체를 사용한다고 명시함.
    def __init__(
        self, user_repo: IUserRepository, email_service: EmailService
    ):  # 컨테이너에 등록한 user repo를 사용할 수 있게 됨., 그리고 명시하지 않아도 자동으로 등록됨.
        self.email_service = email_service
        self.user_repo = user_repo
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(
        self,
        # background_tasks: BackgroundTasks,
        name: str,
        email: str,
        password: str,
        memo: str | None = None,
    ):

        _user = None
        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e

        if _user:
            raise HTTPException(status_code=422, detail="이미 사용 중인 이메일입니다.")

        now = datetime.now()

        user: User = User(
            id=self.ulid.generate(),
            profile=Profile(name=name, email=email),
            password=self.crypto.encrypt(password),
            memo=memo,
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)

        # background_tasks.add_task(self.email_service.send_email, user.profile.email)

        SendWelcomeEmailTask().run(user.profile.email)

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

    def delete_user(self, user_id: str):
        self.user_repo.delete_user(user_id)

    def login(self, email: str, password: str):
        user = self.user_repo.find_by_email(email)
        if not self.crypto.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        access_token = create_access_token(payload={"user_id": user.id}, role=Role.USER)

        return access_token
