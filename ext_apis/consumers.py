import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class MpesaTransactionConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.receipt_id = self.scope['url_route']['kwargs']['receipt_id']
        self.group_name = f"transaction_{self.receipt_id}"

        # Join a group specific to this transaction
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive transaction update from group
    async def transaction_update(self, event):
        # Send the update to the WebSocket client
        await self.send_json(event)
