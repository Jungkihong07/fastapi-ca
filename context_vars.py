from contextvars import ContextVar

""" 유저의 정보를 저장할 콘텍스트, 토큰 없이 수행되는 API 경우 None이 된다. """
user_context: dict | None = ContextVar("current_user", default=None)
