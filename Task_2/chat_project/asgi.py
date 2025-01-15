import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import ChatConsumer
from django.urls import path

# Set the default settings module for the 'django' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')

# Define the ASGI application to route HTTP and WebSocket connections.
application = ProtocolTypeRouter({
    'http': get_asgi_application(),  # Handle HTTP requests
    'websocket': AuthMiddlewareStack(  # Handle WebSocket connections
        URLRouter([
            path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),  # Define WebSocket route
        ])
    ),
})
