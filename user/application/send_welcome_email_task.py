from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from celery import Task
from config import get_settings


settings = get_settings()


# 샐러리에서 제공하는 `Task` 클래스를 상속받았다. 이제 이 클래스는 샐러리 테스크로 동작한다.
class SendWelcomeEmailTask(Task):
    #  태스크 내에서 유일한 값을 가지는 이름을 부여한다. 이름을 지정하지 않으면, 샐러리는 태스크를 찾지 못한다.
    name = "send_welcome_email_task"

    # 태스크가 수행될 때 run 함수가 호출된다. 이메일 발송은 EmailService에서 구현한 바와 동일하다.
    def run(self, receiver_email: str):
        sender_email = "hnn07185@gmail.com"
        password = settings.email_password

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        # 이메일 제목
        message["Subject"] = "회원 가입을 환영합니다."
        # 이메일 내용
        body = "TIL 서비스를 이용해주셔서 감사합니다."
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(message)
