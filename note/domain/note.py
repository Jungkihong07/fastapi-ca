from dataclasses import dataclass
from datetime import datetime


@dataclass
class Tag:
    id: str
    name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Note:
    id: str
    user_id: str
    title: str  # 노트의 제목
    content: str  # 세부 내용
    memo_date: str  # '20231126"과 같이 해당 지식을 얻은 날짜
    tags: list[Tag]  # 해시태그의 역할
    created_at: datetime
    updated_at: datetime
