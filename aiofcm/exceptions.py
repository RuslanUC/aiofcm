class AuthorizationError(Exception):
    def __init__(self, code: int, response: str):
        self.code = code
        self.response = response

    def __str__(self) -> str:
        return f"Failed to authorize! Status code: {self.code}"
