import json

from plant.models import *

from plant.modules.firestoreTools import FireStoreClient

def GeneratePotKey():
    charset = string.ascii_uppercase + string.digits
    return "-".join("".join(random.choice(charset) for _ in range(4)) for _ in range(3))

def InitPotCRUD(request):
    Key         = GeneratePotKey()
    SerialID    = FireStoreClient.InitPotDocuments(Key)
    newPot      = PotRegistry(SerialID=SerialID, Key=Key)
    newPot.save()
    
    return SerialID, Key

def RegisterPotCRUD(request, pot):
    FireStoreClient.Notify(pot.SerialID, "Pot has been registered")
    
    pot.Account = request.user
    pot.save()
    
def GetAllPotCRUD(request):
    return PotRegistry.objects.filter(Account=request.user)