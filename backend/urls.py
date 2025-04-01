from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Djoser authentication endpoints
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
    # User/auth related 
    path('user/', include('account.api.urls')),
    
    # Plant management app
    path('plant/', include('plant.api.urls')),
    
    # Assistant
    path('assistant/', include('assistant.api.urls')),
]
