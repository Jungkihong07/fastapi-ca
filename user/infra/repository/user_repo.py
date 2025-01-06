from database import SessionLocal
from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User as UserVO
from user.infra.db_models.user import User

class UserRepository(IUserRepository):
    def save(self, user:UserVO):
        new_user = User(
            id=user.id,
            name=user.profile.name,
            email=user.profile.email,
            password=user.password,
            created_at=user.created_at,  # 생성일 추가
            updated_at=user.updated_at     # 업데이트일 추가
        )

        with SessionLocal() as db: # try-finally 구문으로 명시적으로 세션을 닫게 해준다. 이는 좋은 습관이므로 기억하도록 하자.
            try:
                db = SessionLocal()
                db.add(new_user)
                db.commit()
            finally:
                db.close()
    
    def find_by_email(self, email: str) -> User:
        pass