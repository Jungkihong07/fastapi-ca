from unittest.mock import Mock, patch
from fastapi import HTTPException
import pytest

from user.domain.user import User as UserVO
from user.infra.db_models.user import User
from user.infra.repository.user_repo import UserRepository
from utils.db_utils import map_user


# 해당 테스트 코드는 SQLALchmey의 세션을 모의한 픽스처를 제공한다.
@pytest.fixture
def mock_session_local():
    with patch(
        "user.infra.repository.user_repo.SessionLocal", autospec=True
    ) as mock_session:
        yield mock_session


def test_find_by_email_user_exists(mock_session_local):
    mock_user = User(id=1, email="test@example.com", name="Test User")
    mock_db = Mock()
    # 유저 저장소가 검색결과로 반환되는 유저 도메인 객체를 모의힌다.
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    # 생성되는 세션을 모의힌다.
    mock_session_local.return_value.__enter__.return_value = mock_db

    user_repository = UserRepository()

    result = user_repository.find_by_email("test@example.com")

    assert result == map_user(mock_user)


def test_find_by_email_user_does_not_exist(mock_session_local):
    mock_db = Mock()
    # 유저 저장소의 검색 결과를 None으로 설정한다.
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_session_local.return_value.__enter__.return_value = mock_db
    user_repository = UserRepository()

    # 예외가 일어났는지 확인한다.
    with pytest.raises(HTTPException) as exception:
        user_repository.find_by_email("nonexistent@exmple.com")

    assert exception.value.status_code == 422
