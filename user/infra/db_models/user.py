from datetime import datetime
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(String(36), primary_key=True)  # 기본 키 (UUID 또느 ULID 같은 문자열을 사용할 것이기 때문에 string)
    name: Mapped[str] = mapped_column(String(32), nullable=False)  # 이름
    email: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)  # 이메일 (고유)
    password: Mapped[str] = mapped_column(String(64), nullable=False)  # 비밀번호
    memo: Mapped[str] = mapped_column(Text, nullable=True)  # 비밀번호
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # 생성일
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # 업데이트일
