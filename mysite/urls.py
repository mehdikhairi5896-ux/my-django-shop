from django.contrib import admin
from django.urls import path
from .views import home, shop, product_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('shop/', shop),
    path('shop/<int:product_id>/', product_detail),
]
