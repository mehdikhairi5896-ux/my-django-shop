from django.urls import path
from . import views

urlpatterns = [
    path("", views.ad_list, name="ad_list"),
    path("create/", views.ad_create, name="ad_create"),
    path("<int:ad_id>/", views.ad_detail, name="ad_detail"),
    path("<int:ad_id>/edit/", views.ad_edit, name="ad_edit"),
    path("<int:ad_id>/delete/", views.ad_delete, name="ad_delete"),
    path("<int:ad_id>/pay/", views.pay_ad, name="pay_ad"),
    path("<int:ad_id>/test-pay/", views.test_payment, name="test_payment"),
    path("verify/", views.verify_payment, name="verify_payment"),
]

