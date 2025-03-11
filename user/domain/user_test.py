from datetime import datetime
from user.domain.user import User, Profile


def test_user_creation():
    user = User(
        id="ID_DEXTER",
        profile=Profile(name="Dexter", email="dexter@example.com"),
        password="password1234",
        memo=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    assert user.id == "ID_DEXTER"
    assert user.profile.name == "Dexter"
    assert user.profile.email == "dexter@example.com"
    assert user.password == "password1234"
    assert user.memo is None  # None에 대해서 나중에 분석 포스팅을 해보자.
