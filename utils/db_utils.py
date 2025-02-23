from datetime import datetime
from sqlalchemy import inspect
from user.domain.user import User as UserVO, Profile


# 자동으로 할당되어 만들어주는 코드로 보인다.
def row_to_dict(row) -> dict:
    return {key: getattr(row, key) for key in inspect(row).attrs.keys()}


# user mapping 함수 # 해당 코드는 나중에 data_mapper.py 로 파일을 따로 만들어서 관리하거나 하자.
def map_user(row) -> UserVO:
    user_dict = row_to_dict(row)

    # Profile 객체 생성
    profile = Profile(name=user_dict["name"], email=user_dict["email"])

    # User 객체 생성
    user = UserVO(
        id=user_dict["id"],
        profile=profile,
        password=user_dict["password"],
        memo=user_dict["memo"],
        created_at=user_dict["created_at"],
        updated_at=user_dict["updated_at"],
    )

    return user
