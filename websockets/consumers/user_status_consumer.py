import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from asgiref.sync import sync_to_async

from core.models import User
from profiles.models import Profile
from profiles.serializers import UserSerializer


@sync_to_async
def update_user_online_status_to_true(user):
    return User.objects.filter(id=user.id).update(is_online=True)


@sync_to_async
def update_user_online_status_to_false(user):
    return User.objects.filter(id=user.id).update(is_online=False)


@sync_to_async
def online_users_list(user):
    return UserSerializer(
        User.objects.filter(is_online=True).exclude(id=user.id),
        many=True,
        source="user"
    ).data


class UserStatus(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.user = self.scope["client"]
        await update_user_online_status_to_true(self.user)
        await self.send(json.dumps({"is_online": True}))

    async def disconnect(self, close_code):
        await update_user_online_status_to_false(self.user)

    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        if online_users := await online_users_list(self.user):
            await self.send(json.dumps({"online_users": online_users}))
        else:
            await self.send(json.dumps({}))
