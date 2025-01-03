from dataclasses import dataclass
from datetime import datetime

#  id 속성이 없고, 데이터만 가지고 있는 데메인 객체를 값 객체라고 함.
@dataclass
class Profile:
    name: str
    email: str

# 도메인 객체를 다루기 쉽게 하기 위하여 dataclass로 선언하였음.
@dataclass
class User:
    id: str
    profile: Profile
    # name: str
    # email: str
    password: str
    created_at: datetime
    updated_at : datetime
