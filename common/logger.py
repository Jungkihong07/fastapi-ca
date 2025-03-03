import logging
from context_vars import user_context


log_format = "%(asctime)s %(name)s %(levelname)s:\tuser: %(user)s: %(message)s"

""" 기본 포매터를 상속받아 따로 정의한다. 이렇게 하는 이유는 log_format에 있는 %(user)s:가 있는 데, 이 때문에 유비콘이 새로 시작하는 과정에서 에러가 발생하기 때문
    LogRecord가 우리가 추가한 user 속성이 없는 경우를 처리해준다. -> class CustomFormatter(logging.Formatter):"""


# 커스텀 포매터
class CustomFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "user"):
            record.user = "Anonymous"
        return super().format(record)


"""  """
# 커스텀 핸들러
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter(log_format))

# 커스텀 로거 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


""" 이 부분이 핵심. 기본 콘텍스트 필터를 상속받은 필터를 별로도 정의한다. 이때 filter 함수에 전달되는 LogRecord객체 우리가 원하는 user 속성을 추가한다. """


# 커스텀 콘텍스트 필터
class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        record.user = str(user_context.get())
        return True


# 따로 정의한 콘텍스트 필터를 로거에 추가한다.
logger.addFilter(ContextFilter())
