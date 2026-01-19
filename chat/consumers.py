from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.nome_sala = self.scope['url_route']['kwargs']['nome_sala']
        self.grupo_sala = f'chat_{self.nome_sala}'

        # Join room group
        await self.channel_layer.group_add(
            self.grupo_sala,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.grupo_sala,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mensagem = text_data_json['mensagem']

        # Send message to room group
        await self.channel_layer.group_send(
            self.grupo_sala,
            {
                'type': 'chat_message',
                'message': mensagem
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        mensagem = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': mensagem
        }))