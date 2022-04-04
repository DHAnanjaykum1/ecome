from django.urls import path 
from .views import *


app_name = "core"

urlpatterns = [
     path("",HomeView.as_view(),name="homepage"),
     path("products/<slug>/",ItemDetailsView.as_view(),name="item"),
     path("order-summary/",OrderSummaryVIew.as_view(),name="order-summary"),
     path("checkout/",CheckOutView.as_view(),name="checkout"),
     path("save-address-action/",save_Address_Action,name="save_Address_Action"),
     path("add-to-cart/<slug>/",AddToCart.as_view(),name="add-to-cart"),
     path("remove-from-cart/<slug>/",RemoveFromCart.as_view(),name="remove-from-cart"),
     path("minus-from-cart/<slug>/",MinusItemCart.as_view(),name="minus-from-cart"),
     path("add-coupon/",AddCouponView.as_view(),name="add-coupon"),
     path("remove-coupon/",RemoveCouponView.as_view(),name="remove-coupon"),
]