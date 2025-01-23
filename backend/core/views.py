from django.urls import path
from core import views
from django.shortcuts import render

def landing_page(request):
    return render(request, 'base.html')  # Ensure 'base.html' exists and is correctly referenced