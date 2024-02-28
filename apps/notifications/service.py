from fastapi import BackgroundTasks
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig

from apps.notifications.schemas import EmailSchema
from settings.email_settings import EMAIL_SETTINGS


class EmailNotificationService:
    """Сервис для рассылки уведомлений по почте"""
    conf = ConnectionConfig(
        MAIL_FROM=EMAIL_SETTINGS['MAIL_USERNAME'],
        MAIL_USERNAME=EMAIL_SETTINGS['MAIL_USERNAME'],
        MAIL_PASSWORD=EMAIL_SETTINGS["MAIL_PASSWORD"],
        MAIL_PORT=int(EMAIL_SETTINGS["MAIL_PORT"]),
        MAIL_SERVER=EMAIL_SETTINGS["MAIL_SERVER"],
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
    )

    async def write_notification(self, email: EmailSchema):
        message = MessageSchema(
            subject=email.subject,
            recipients=email.recipients,
            body=email.message,
            subtype="plain"
        )

        fm = FastMail(self.conf)
        await fm.send_message(message)
        print(message)

    async def send_notification(self, email: EmailSchema, background_tasks: BackgroundTasks) -> None:
        background_tasks.add_task(self.write_notification, email)
