from djangourls import path
from .consumers import ChatConsumer
from .consumers import AuctionConsumer

websocket_urlpatterns = [
    path("ws/auction/<int:auction_id>/", AuctionConsumer.as_asgi()),
    path("ws/chat/<int:seller_id>/", ChatConsumer.as_asgi()),
]