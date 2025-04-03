from djoser.serializers import UserCreateSerializer
from rest_framework.serializers import ModelSerializer       
from account.models import *

# Get custom user model
from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password') 
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ("email", "Name", "PhoneNumber", "DateOfBirth", "Gender", "Address", "Avatar") 