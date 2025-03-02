from sqlalchemy import Column, DateTime, ForeignKey, String, Table, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

""" 노트와 태그의 다대다 관계를 나타내기 위한 연결 테이블 """
note_tag_association = Table(
    "Note_Tag",
    Base.metadata,
    Column("note_id", String(36), ForeignKey("Note.id")),
    Column("tag_id", String(36), ForeignKey("Tag.id")),
)


class Note(Base):
    __tablename__ = "Note"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    title = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    memo_date = Column(String(8), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    """ relationship 함수를 이용해 다대다 관계를 맺는다. """
    tags = relationship(
        "Tag",
        secondary=note_tag_association,
        back_populates="notes",  # 해당 옵션을 사용하여 노트 객체를 가져올 때 연관된 태그 객체도 모두 가져온다.
        lazy="joined",
    )


class Tag(Base):
    __tablename__ = "Tag"

    id = Column(String(36), primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    """ 다대다 관계 설정을 한다. """
    notes = relationship(
        "Note",
        secondary=note_tag_association,
        back_populates="tags",
        lazy="joined",
    )
