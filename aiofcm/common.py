from typing import Optional, Dict, Any, TypedDict


class AppConfig(TypedDict):
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    token_uri: Optional[str]


class Message:
    __slots__ = (
        "token",
        "topic",
        "condition",
        "notification",
        "data",
    )

    def __init__(
        self,
        device_token: Optional[str] = None,
        topic: Optional[str] = None,
        condition: Optional[str] = None,
        notification: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, str]] = None,
    ):
        check = [device_token, topic, condition]
        if check.count(None) != 2:
            raise ValueError("One of (device_token, topic, condition) should be provided")

        self.token = device_token
        self.topic = topic
        self.condition = condition
        self.notification = notification
        self.data = data

    def as_dict(self) -> Dict[str, Any]:
        result = {}

        for field in (
            "token",
            "topic",
            "condition",
            "notification",
            "data",
        ):
            value = getattr(self, field, None)
            if value is not None:
                result[field] = value

        return result
