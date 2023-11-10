from fastapi import Request, HTTPException
from pydantic import EmailStr
from config.config import settings
import httpx


class NotificationClient:
    register_url = settings.NOTIFICATION_REGISTER_URL
    reset_password_url = settings.NOTIFICATION_RESET_PASSWORD_URL

    async def _send_notification(self, url: str, email: EmailStr, request: Request):
        headers = {'correlation-id': request.state.correlation_id}
        async with httpx.AsyncClient(headers=headers) as client:
            try:
                response = await client.post(url, json={'email': email})
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as exc:
                raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)

    async def notification_register(self, email: EmailStr, request: Request):
        return await self._send_notification(self.register_url, email, request)

    async def notification_reset_password(self, email: EmailStr, request: Request):
        return await self._send_notification(self.reset_password_url, email, request)


def get_notification_client():
    return NotificationClient()
