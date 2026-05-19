import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from rooms import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangochat.settings')

application = {
    'http': get_asgi_application(),
    'websockets': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
}


