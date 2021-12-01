# mysite/asgi.py
import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chats.routing
from .wsgi import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imate.settings")
# django.setup()
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chats.routing.websocket_urlpatterns
        )
    ),
})

# import os
# import django
# import channels.routing

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourappname.settings")
# django.setup()
# application = channels.routing.get_default_application()