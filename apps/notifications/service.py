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

    @classmethod
    async def __task_send_message(cls, email: EmailSchema):
        message = MessageSchema(
            subject=email.subject,
            recipients=email.recipients,
            body=email.message,
            subtype="plain"
        )
        fm = FastMail(cls.conf)
        await fm.send_message(message)

    @classmethod
    async def send_notification(cls, email: EmailSchema, background_tasks: BackgroundTasks = None) -> None:
        if background_tasks:
            background_tasks.add_task(cls.__task_send_message, email)
        else:
            await cls.__task_send_message(email)
