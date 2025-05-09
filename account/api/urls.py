from django.urls import path

# Importing related views
from . import views

# Setting up urls patterns
urlpatterns = [
    # User related endpoints
    path('updateinfo/', views.EditUserInfo),
    path('info/',       views.GetUserInfo),
]