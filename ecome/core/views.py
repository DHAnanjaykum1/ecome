from re import template
from django.shortcuts import render
from django.views.generic import ListView
from .models import Item

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


