import json

from django.db.models import Q

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
    
    FireStoreClient.Notify(SerialID, "Pot has been manufactured")
    
    return SerialID, Key

def RegisterPotCRUD(request, pot):
    FireStoreClient.Notify(pot.SerialID, "Pot has been registered")
    
    pot.Account = request.user
    pot.save()
    
def GetAllPotCRUD(request):
    return PotRegistry.objects.filter(Account=request.user)

def CreatePlanCRUD(request):
    dict = request.body.decode("UTF-8")
    planInfo = json.loads(dict)
    
    planName = planInfo["Name"]
    planJSONstring = json.dumps(planInfo)  
    
    newPlan = Plan(Name=planName, JSON=planJSONstring, Account=request.user)
    newPlan.save()
    
def EditPlanCRUD(request):
    dict = request.body.decode("UTF-8")
    planInfo = json.loads(dict)
    
    planID = planInfo.pop("planID", None)
    planName = planInfo["Name"]
    planJSONstring = json.dumps(planInfo)  
    
    plan = Plan.objects.get(id=planID)
    plan.Name = planName
    plan.JSON = planJSONstring
    plan.save()

def GetAllPlansCRUD(request):
    return Plan.objects.filter(Q(Account=request.user) | Q(Account=None))
    
def DeletePlanCRUD(request):
    dict = request.body.decode("UTF-8")
    planInfo = json.loads(dict)
    planID = planInfo["planID"]
    plan = Plan.objects.get(id=planID)
    plan.delete()
    
def ApplySettingsCRUD(request):
    dict = request.body.decode("UTF-8")
    settingsInfo = json.loads(dict)
    
    pot = PotRegistry.objects.get(id=settingsInfo['potID'])
    pot.Name = settingsInfo['Name']
    pot.save()
    
    plan = Plan.objects.get(id=settingsInfo['planID'])
    FireStoreClient.ApplyPlan(pot.SerialID, plan.JSON, pot.Key)
    
def DisownPotCRUD(potID):    
    pot = PotRegistry.objects.get(id=potID)
    pot.Account = None
    pot.save()
    
def AddTemperatureCRUD(request):
    dict = request.body.decode("UTF-8")
    entryInfo = json.loads(dict)
    
    serialID = entryInfo['SerialID']
    template = {
        "Time": entryInfo['Time'],
        "Value": entryInfo['Value']
    }
    
    FireStoreClient.addTemperatureEntry(template, serialID)