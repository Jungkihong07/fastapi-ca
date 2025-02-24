from fastapi import HTTPException
from utils.db_utils import row_to_dict, map_user
from database import SessionLocal
from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User as UserVO, Profile
from user.infra.db_models.user import User


class UserRepository(IUserRepository):
    def save(self, user: UserVO):
        new_user = User(
            id=user.id,
            name=user.profile.name,
            email=user.profile.email,
            password=user.password,
            memo=user.memo,
            created_at=user.created_at,  # 생성일 추가
            updated_at=user.updated_at,  # 업데이트일 추가
        )

        with SessionLocal() as db:  # try-finally 구문으로 명시적으로 세션을 닫게 해준다. 이는 좋은 습관이므로 기억하도록 하자.
            try:
                db = SessionLocal()
                db.add(new_user)
                db.commit()
            finally:
                db.close()

    def find_by_email(self, email: str) -> UserVO:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=422)

        return map_user(user)

    def find_by_id(self, id: str) -> UserVO:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()

        if not user:
            raise HTTPException(status_code=422)

        return map_user(user)

    def update(self, user_vo: UserVO):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_vo.id).first()

        if not user:
            raise HTTPException(status_code=422)

        user.name = user_vo.profile.name
        user.password = user_vo.password

        db.add(user)
        db.commit()

        return user

    def get_users(
        self, page: int = 1, items_per_page: int = 10
    ) -> tuple[int, list[UserVO]]:
        with SessionLocal() as db:
            query = db.query(User)
            total_count = query.count()

            offset = (page - 1) * items_per_page
            users = query.limit(items_per_page).offset(offset).all()

        return total_count, [map_user(user) for user in users]

    def delete_user(self, id: str):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()

            if not user:
                raise HTTPException(status_code=422)

            db.delete(user)
            db.commit()
