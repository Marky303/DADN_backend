import json

from django.db.models import Q

from plant.models import *

from plant.modules.firestoreTools import FireStoreClient
from datetime import datetime

from plant.models import *

def RegisterPotCRUD(request, pot):
    try:
        FireStoreClient.Notify(pot.SerialID, "Pot has been registered")
        pot.Account = request.user
        pot.save()
    except Exception as e:
        raise Exception("Error")
