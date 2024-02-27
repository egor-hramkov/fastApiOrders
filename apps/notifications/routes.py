from fastapi import APIRouter, BackgroundTasks

from apps.notifications.schemas import EmailSchema
from apps.notifications.service import EmailNotificationService

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)

email_notification_service = EmailNotificationService()


@router.post("/send-email/")
async def send_notification(email: EmailSchema, background_tasks: BackgroundTasks):
    await email_notification_service.send_notification(email, background_tasks)
    return {"message": "Notification sent in the background"}
