import os

from fastapi.exceptions import HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.email.mail_username,
    MAIL_PASSWORD=settings.email.mail_password,
    MAIL_FROM=settings.email.mail_from,
    MAIL_PORT=settings.email.mail_port,
    MAIL_SERVER=settings.email.mail_server,
    MAIL_FROM_NAME=settings.email.mail_from_name,
    MAIL_STARTTLS=settings.email.mail_starttls,
    MAIL_SSL_TLS=settings.email.mail_ssl_tls,
    USE_CREDENTIALS=settings.email.use_credentials,
    VALIDATE_CERTS=settings.email.validate_certs,
    TEMPLATE_FOLDER=os.path.join(os.getcwd(), "templates", "email"),
)


async def send_change_password_email(email_to: str, new_password: str) -> bool:
    try:
        template_path = os.path.join(
            conf.TEMPLATE_FOLDER, "mail_template.html"
        )
        with open(template_path, "r", encoding="utf-8") as file:
            html_template = file.read()
        html = html_template.replace("%new_password%", new_password)

        message = MessageSchema(
            subject="Пароль был изменён",
            recipients=[email_to],
            body=html,
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
