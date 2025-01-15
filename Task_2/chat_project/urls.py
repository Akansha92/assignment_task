from django.contrib import admin
from django.urls import path, include
from chat.views import chat_view  # Import your chat view or home view

urlpatterns = [
    path('', include('chat.urls')),  # Include the chat app URLs
    path('admin/', admin.site.urls),
    path('signup/', include('chat.urls')),  # Assuming signup is handled in chat.urls
    path('login/', include('chat.urls')),  # Assuming login is handled in chat.urls
    path('logout/', include('chat.urls')),  # Assuming logout is handled in chat.urls
    path('chat/', include('chat.urls')),  # Chat-specific URLs
    path('', chat_view, name='home'),  # Map root URL to chat_view or home view
]