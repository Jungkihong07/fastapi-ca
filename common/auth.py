from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jose import JWTError, jwt
from enum import StrEnum
from dataclasses import dataclass


class Role(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


SECRET_KEY = "THIS_IS_SUPER_SECRET_KEY"
ALGORITHM = "HS256"


def create_access_token(
    payload: dict,
    role: Role,
    expires_delta: timedelta = timedelta(hours=6),
):
    expire = datetime.now(timezone.utc) + expires_delta
    payload.update(
        {
            "role": role,
            "exp": expire,
        }
    )  # 토큰의 만료 시간을 페이로드에 추가한다. 유저가 게시물을 작성하는 긴 시간을 고려하여 6시간으로 고려
    encoded_jwt = jwt.encode(
        payload, SECRET_KEY, algorithm=ALGORITHM
    )  # 외부에 공개하는 않는 보안키를 사용해 암호화
    return encoded_jwt


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


""" 
    FASTAPI가 제공하는 OAUTH2PasswordBeaer 클래스를 이용해 아이디, 패스워드 기반으로 로그인할 수 있도록 한다.
    tokenUrl은 앞서 만든 토큰을 발근하는 엔드포인트가 할당돼 있다.
"""
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")


""" 토큰의 페이로드에 있는 정보를 담을 데이터 클래스이다. """


@dataclass
class CurrentUser:
    id: str
    role: Role


def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    role = payload.get("role")
    # 페이로드에 필요한 정보가 없거나, 역할이 일반 유저의 역할이 아니면 403 에러를 일으킨다.
    if not user_id or not role or role != Role.USER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return CurrentUser(user_id, Role(role))


# admin 구별하는
def get_admin_user(token: Annotated[str, Depends(oauth2_schema)]):
    payload = decode_access_token(token)

    role = payload.get("role")
    if not role and role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return CurrentUser("ADMIN_USER_ID", role)
