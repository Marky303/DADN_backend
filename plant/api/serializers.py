from rest_framework.serializers import ModelSerializer       
from plant.models import *

# Pot serializer
class PotRegistrySerializer(ModelSerializer):
    class Meta:
        model = PotRegistry
        fields = ("id", "Name", "SerialID", "Key")
        
class PlanSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = ("id", "Name", "JSON")