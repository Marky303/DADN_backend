from django.urls import path

# Importing related views
from . import views

# Setting up urls patterns
urlpatterns = [
    # Manufacturer related endpoints
    path('init/', views.InitPot),
    
    # Plant related endpoints
    path('register/', views.RegisterPot),
    path('getallpots/', views.GetAllPots),
    path('applysettings/', views.ApplySettings),
    path('disownpot/', views.DisownPot),
    
    # Plan related endpoints
    path('createplan/', views.CreatePlan),
    path('getallplans/', views.GetAllPlans),
    path('editplan/', views.EditPlan),
    path('deleteplan/', views.DeletePlan),
]