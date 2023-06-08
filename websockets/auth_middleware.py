import jwt
import uuid

from django.conf import settings

from channels.db import database_sync_to_async

from core.models import User


@database_sync_to_async
def return_user(token_string):
    try:
        payload = jwt.decode(
            token_string, settings.SECRET_KEY, algorithms=['HS256']
        )
        user = User.objects.get(id=payload['user_id'])
        return user
    except jwt.ExpiredSignatureError:
        return None


class TokenAuthMiddleWare:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        token = headers[b'authorization'].decode().split()[1]
        user = await return_user(token)
        scope["client"] = user
        scope["session_id"] = uuid.uuid4()
        return await self.app(scope, receive, send)
