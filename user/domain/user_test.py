from datetime import datetime
from user.domain.user import User


def test_user_creation():
    user = User(
        id="ID_DEXTER",
        name="Dexter",
        email="dexter@exmple.com",
        password="password1234",
        memo=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    assert user.id == "ID_DEXTER"
    assert user.name == "Dexter"
    assert user.email == "dexter@exmple.com"
    assert user.password == "password1234"
    assert user.memo is None  # None에 대해서 나중에 분석 포스팅을 해보자.
