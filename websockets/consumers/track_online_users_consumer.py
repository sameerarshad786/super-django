import json

from django.contrib.gis.geos import Point

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from asgiref.sync import sync_to_async

from core.models import User, UserSensitiveInformation
from profiles.serializers import UserSerializer
from ..http_request import Request
from ..pagination import paginate_response


@sync_to_async
def online_users_list(user, location):
    if location:
        longitude = location["longitude"]
        latitude = location["latitude"]
        UserSensitiveInformation.objects.filter(
            user=user).update(point=Point(float(longitude), float(latitude)))
    return UserSerializer(
        User.objects.filter(is_online=True).exclude(id=user.id),
        many=True,
        source="user",
        context={'request': Request()}
    ).data


class TrackOnlineUsers(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        await User.objects.filter(id=self.user.id).aupdate(is_online=True)
        count = await User.objects.filter(
            is_online=True).exclude(id=self.user.id).acount()
        online_users = await online_users_list(self.user, location=None)
        paginted_response = await paginate_response(
            count, 1, online_users)
        await self.send(json.dumps({"online_users": paginted_response}))

    async def disconnect(self, close_code):
        await User.objects.filter(id=self.user.id).aupdate(is_online=False)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        page_number = text_data_json.get("page_number", 1)
        count = await User.objects.filter(
            is_online=True).exclude(id=self.user.id).acount()
        location = text_data_json["location"]
        online_users = await online_users_list(self.user, location)
        paginted_response = await paginate_response(
            count, page_number, online_users)
        await self.send(json.dumps({"online_users": paginted_response}))
