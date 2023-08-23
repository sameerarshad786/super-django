import jwt
import uuid

from urllib.parse import parse_qs

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
        query_string = scope["query_string"].decode()
        query_params = parse_qs(query_string)

        try:
            conversation_id = query_params["conversation_id"][0]
        except KeyError:
            conversation_id = None

        try:
            parent_id = query_params["parent_id"][0]
        except KeyError:
            parent_id = None

        token = query_params["token"][0]
        user = await return_user(token)
        scope["user"] = user
        scope["session_id"] = uuid.uuid4()
        scope["conversation_id"] = conversation_id
        scope["parent_id"] = parent_id
        return await self.app(scope, receive, send)
