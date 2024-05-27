import json
from base64 import urlsafe_b64encode
from time import time

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from aiofcm.common import AppConfig


def itime() -> int:
    return int(time())


def create_jwt(config: AppConfig):
    key = load_pem_private_key(config["private_key"].encode("utf8"), None, default_backend())

    header = {"alg": "RS256", "typ": "JWT", "kid": config["private_key_id"]}
    payload = {
        "iss": config["client_email"],
        "scope": "https://www.googleapis.com/auth/firebase.messaging",
        "aud": "https://oauth2.googleapis.com/token",
        # 1 hour, see "Required claims" -> exp at
        # https://developers.google.com/identity/protocols/oauth2/service-account#httprest
        "exp": itime() + 60 * 60,
        "iat": itime(),
    }

    header = urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode("utf8")).decode("utf8")
    payload = urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode("utf8")).decode("utf8")

    signature = f"{header}.{payload}".encode("utf8")
    signature = key.sign(signature, PKCS1v15(), SHA256())
    signature = urlsafe_b64encode(signature).decode("utf8")

    return f"{header}.{payload}.{signature}"
