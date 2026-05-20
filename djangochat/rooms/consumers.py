import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import  sync_to_async
from .models import Room, Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = data['username']
        message = data['message']
        room = data['room']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'room': room,
            }
        )

    async def chat_message(self, event):
        user = event['user']
        message = event['message']
        room = event['room']

        # 💡 Added 'await' here to ensure database insertion finishes properly!
        await self.create_messages(room_slug=room, username=user, message=message)

        await self.send(text_data=json.dumps({
            'message': message,
            'username': user,  # ✅ FIXED: Changed 'user' to 'username' to perfectly match your JS frontend!
            'room': room,
        }))

    @sync_to_async
    def create_messages(self, room_slug, username, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room_slug)

        Message.objects.create(room=room, user=user, content=message)