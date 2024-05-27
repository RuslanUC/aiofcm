import asyncio
import logging

from aiofcm import FCM, Message

APP_CONFIG = {
    "project_id": "some-app-12345",
    "private_key_id": "217bd0c4969983f2077ef73847ce353956aacb28",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-12345@some-app-12345.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com/token",
}


def setup_logger(log_level):
    log_level = getattr(logging, log_level)
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)8s %(module)6s:%(lineno)03d %(message)s",
        level=log_level,
    )


if __name__ == "__main__":
    setup_logger("DEBUG")

    device_token = "<DEVICE_TOKEN>"

    notification = {
        "title": "Hello from Firebase",
        "body": "This is notification",
    }

    fcm = FCM(APP_CONFIG)

    async def send_message():
        message = Message(
            device_token=device_token,
            notification=notification,
        )
        await fcm.send_message(message)

    async def main():
        send_messages = [send_message() for _ in range(1000)]
        import time

        t = time.time()
        await asyncio.wait(send_messages)
        print("Done: %s" % (time.time() - t))
        print()

    try:
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(main())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
