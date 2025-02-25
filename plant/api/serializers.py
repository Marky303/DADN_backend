from rest_framework.serializers import ModelSerializer       
from plant.models import *

# Pot serializer
class PotRegistrySerializer(ModelSerializer):
    class Meta:
        model = PotRegistry
        fields = ("id", "Name", "SerialID")