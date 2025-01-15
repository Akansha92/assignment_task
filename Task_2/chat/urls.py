from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/', views.chat_view, name='chat'),
    path('chat/<str:username>/', views.chat_view, name='chat_with_user'),
    path('send_message/<str:username>/', views.send_message, name='send_message'),
]
