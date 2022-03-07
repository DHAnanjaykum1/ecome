from django.urls import path 
from .views import *


app_name = "core"

urlpatterns = [
     path("",HomeView.as_view(),name="homepage"),
     path("products/<slug>/",ItemDetailsView.as_view(),name="item"),
]
