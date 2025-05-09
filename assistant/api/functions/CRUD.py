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
    
def GetAllPotsCRUD(request):
    user = request.user
    pots = PotRegistry.objects.filter(Account=user)
    return pots

def FindPotsCRUD(request, name, serialID):
    filters = Q(Account=request.user)
    if name:
        filters &= Q(Name__icontains=name)
    if serialID:
        filters &= Q(SerialID=serialID)  
    return PotRegistry.objects.filter(filters)

def CreatePlanCRUD(request, plan):
    planName = plan["Name"]
    planJSONstring = json.dumps(plan)  
    
    newPlan = Plan(Name=planName, JSON=planJSONstring, Account=request.user)
    newPlan.save()

def FindPlansCRUD(request, name):
    filters = Q(Account=request.user) | Q(Account=None)
    if name:
        filters &= Q(Name__icontains=name)
    return Plan.objects.filter(filters)
