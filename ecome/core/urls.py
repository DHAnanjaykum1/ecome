from django.urls import path 
from .views import *


app_name = "core"

urlpatterns = [
     path("",HomeView.as_view(),name="homepage"),
     path("products/<slug>/",ItemDetailsView.as_view(),name="item"),
     path("order-summary/",OrderSummaryVIew.as_view(),name="order-summary"),
     path("add-to-cart/<slug>/",AddToCart.as_view(),name="add-to-cart"),
]
