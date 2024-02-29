import asyncio

from fastapi import APIRouter, BackgroundTasks, Depends
from starlette.requests import Request
from sse_starlette.sse import EventSourceResponse

from apps.auth.oauth2 import OAuth2
from apps.notifications.factory import NotificationFactory
from apps.notifications.schemas import EmailSchema
from apps.notifications.service import EmailNotificationService
from apps.user.schemas import UserOutModel
from redis_layer.redis_client import RedisClient

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)

email_notification_service = EmailNotificationService()


@router.post("/send-email/")
async def send_notification(email: EmailSchema, background_tasks: BackgroundTasks):
    """Отправка сообщений по электронной почте"""
    await email_notification_service.send_notification(email, background_tasks)
    return {"message": "Notification sent in the background"}


@router.get("/sse")
async def message_stream(request: Request, current_user: UserOutModel = Depends(OAuth2().get_current_user)):
    async def notification_generator():
        MESSAGE_STREAM_DELAY = 5  # second
        while True:
            if await request.is_disconnected():
                break
            notifications: dict = await RedisClient.get_notifications(current_user.id)
            if notifications:
                notification_class = await NotificationFactory.get_notification_class(notifications)
                yield notification_class.build_notification()
                await RedisClient.delete_sent_notifications(str(current_user.id), notification_class.notification_type)

            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    return EventSourceResponse(notification_generator())
