import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from .models import Auction, Bid

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope["url_route"]["kwargs"]["auction_id"]
        self.room_group_name = f"auction_{self.auction_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        bid_amount = float(data["bid_amount"])
        user = self.scope["user"]

        try:
            auction = await Auction.objects.aget(id=self.auction_id)

            if not auction.is_active:
                return

            if bid_amount > auction.current_price:
                bid = await Bid.objects.acreate(
                    auction=auction,
                    bidder=user,
                    amount=bid_amount,
                )

                # Update auction price
                auction.current_price = bid_amount
                await auction.asave()

                # Broadcast new bid data
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "broadcast_bid",
                        "bid_amount": bid_amount,
                        "bidder": user.username,
                    },
                )

        except ObjectDoesNotExist:
            pass

    async def broadcast_bid(self, event):
        await self.send(text_data=json.dumps(event))
