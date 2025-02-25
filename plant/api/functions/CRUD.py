import json

from plant.models import *

from plant.modules.firestoreTools import FireStoreClient

def InitPotCRUD(request):
    SerialID    =  FireStoreClient.InitPotDocuments()
    newPot      = PotRegistry(SerialID=SerialID)
    newPot.save()
    
    FireStoreClient.Notify(SerialID, "Pot has been registered")
    
    return SerialID, newPot.Key

def RegisterPotCRUD(request, pot):
    pot.Account = request.user
    pot.save()
    
def GetAllPotCRUD(request):
    return PotRegistry.objects.filter(Account=request.user)