import json

from plant.models import *

from plant.modules.firestoreTools import FireStoreClient

def InitPotCRUD(request):
    SerialID    =  FireStoreClient.InitPotDocuments()
    newPot      = PotRegistry(SerialID=SerialID)
    newPot.save()
    return SerialID, newPot.Key

def RegisterPotCRUD(request, pot):
    pot.Account = request.user
    pot.save()