import json
import logging
from time import time
from typing import Optional, Union

from httpx import AsyncClient

from aiofcm.common import Message, AppConfig
from aiofcm.exceptions import AuthorizationError
from aiofcm.utils import create_jwt


class FCM:
    def __init__(self, app_config: Union[str, AppConfig]):
        if isinstance(app_config, dict):
            self._app_config = app_config
        else:
            with open(app_config) as f:
                self._app_config = json.load(f)

        self._access_token: Optional[str] = None
        self._token_expires_at: int = 0

    async def _get_access_token(self) -> str:
        if self._access_token is None or self._token_expires_at < time():
            async with AsyncClient() as cl:
                resp = await cl.post(self._app_config["token_uri"], data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                    "assertion": create_jwt(self._app_config),
                })
                if resp.status_code != 200:
                    raise AuthorizationError(resp.status_code, resp.text)

                self._access_token = resp.json()["access_token"]

        return self._access_token

    async def send_message(self, message: Message) -> Optional[str]:
        # Returns message id

        async with AsyncClient() as cl:
            resp = await cl.post(
                f"https://fcm.googleapis.com/v1/projects/{self._app_config['project_id']}/messages:send",
                headers={"Authorization": f"Bearer {await self._get_access_token()}"},
                json={"message": message.as_dict()},
            )

            if resp.status_code != 200:
                logging.warning(
                    f"Got an error while sending message: "
                    f"status_code={resp.status_code}, response={resp.text}"
                )
                return

            return resp.json()["name"]

    async def send_notification(self, title: str, body: str, image_url: Optional[str] = None,
                                device_token: Optional[str] = None) -> Optional[str]:
        return await self.send_message(Message(
            device_token=device_token,
            notification={
                "title": title,
                "body": body,
                "image": image_url,
            }
        ))

    async def send_data(self, device_token: Optional[str] = None, **kwargs) -> Optional[str]:
        return await self.send_message(Message(
            device_token=device_token,
            data=kwargs
        ))
