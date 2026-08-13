from django.urls import path
from . import views

urlpatterns = [
    path("", views.donation_home, name="donation_home"),
    path("total/", views.donation_total_api, name="donation_total_api"),
]
