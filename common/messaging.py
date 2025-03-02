from celery import Celery
from config import get_settings
from user.application.send_welcome_email_task import SendWelcomeEmailTask

settings = get_settings()

celery = Celery(
    "fastapi-ca",
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
    broker_connection_retry_on_startup=True,  # 브로커와의 연결이 제대로 이루어지지 않으면 재시도를 수행할지에 대한 옵션, True로 설정되면  초기 연결 시도가 실패했을 때 워커가 브로커에 대한 연결을 반복적으로 시도함.
    include=[
        "example.ch10_02.celery_task"
    ],  # include 매개변수를 사용하면 샐러리 태스크가 정의된 모듈을 지정할 수 있음. 태스크를 찾지 못할 때 지정하면 됨.
)
celery.register_task(SendWelcomeEmailTask())
