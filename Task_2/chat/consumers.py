from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.contrib.auth.models import User
from .models import ChatMessage

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        sender_id = data['sender']
        receiver_id = data['receiver']
        message = data['message']

        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)

        ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))
