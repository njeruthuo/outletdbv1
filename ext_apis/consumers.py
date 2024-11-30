from channels.generic.websocket import AsyncWebsocketConsumer
import json


class TransactionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Join the static group for all transaction updates
        self.group_name = "transaction_updates"
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Send a confirmation message to the client
        await self.send(json.dumps({"message": "WebSocket connected"}))

    async def disconnect(self, close_code):
        # Leave the group on disconnect
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Process incoming messages (if necessary)
        data = json.loads(text_data)
        print(f"Message received: {data}")

        # Acknowledge receipt
        await self.send(json.dumps({
            "message": "Acknowledged",
            "details": data,
        }))

    async def send_transaction_update(self, event):
        # Handle transaction updates
        await self.send(json.dumps({
            "type": event["type"],
            "status": event["status"],
            "receipt_id": event["receipt_id"],  # Include receipt ID
            "description": event["description"],
        }))
