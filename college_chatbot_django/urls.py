# college_chatbot/urls.py

from django.contrib import admin
from django.urls import path, include
from chatbot import views as chatbot_views
from chatbot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chatbot/', include('chatbot.urls')),
    path('', views.index, name='index'),  # Add this line to handle the root URL
    path('', chatbot_views.index),  # Loads index.html
]
