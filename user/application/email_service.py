from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from config import get_settings


settings = get_settings()


class EmailService:
    def send_email(self, receiver_email: str):
        sender_email = "hnn07185@gmail.com"
        password = settings.email_password
        """ 
        이 밑에 있는 코드는 smtp 라이브러리와 email 라이브러리르 이용해 메일을 전송하는 구현이다.
        자세한 내용은 https://docs.python.org/ko/3.12/library/email.examples.html 참조
        """
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "회원가입을 환영합니다."

        body = "TIL 서비스를 이용해주셔서 감사합니다."
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(message)
