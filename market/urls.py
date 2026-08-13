from django.urls import path
from . import views

urlpatterns = [
    path("", views.market_list, name="market_list"),
    path("create/", views.market_create, name="market_create"),
    path("<int:item_id>/", views.market_detail, name="market_detail"),
    path("<int:item_id>/buy/", views.market_buy, name="market_buy"),
]
