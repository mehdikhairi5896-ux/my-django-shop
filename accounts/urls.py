from django.urls import path
from .views import profile_view, register

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('register/', register, name='register'),
]
