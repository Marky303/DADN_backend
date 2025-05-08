import json

from django.db.models import Q

from plant.models import *

from plant.modules.firestoreTools import FireStoreClient
from datetime import datetime

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
    entryInfo = json.loads(dict)['data']
    
    serialID = entryInfo['SerialID']
    
    template = {
        "Time": datetime.now().timestamp(),
        "Value": entryInfo['temperature']
    }
    FireStoreClient.addTemperatureEntry(template, serialID)
    
    template['Value'] = entryInfo['light']
    FireStoreClient.addLightEntry(template, serialID)
    
    template['Value'] = entryInfo['moisture']
    FireStoreClient.addMoistureEntry(template, serialID)
    
    template['Value'] = entryInfo['soilHumidity']
    FireStoreClient.addSoilHumidityEntry(template, serialID)
    
def GetPlanCRUD(request):
    dict = request.body.decode("UTF-8")
    info = json.loads(dict)
    serialID = info['SerialID']
    
    return FireStoreClient.getPlan(serialID)

def GetDashboardCRUD(request):
    return {
            "listPlans": {
                "before": [],
                "after": []
        },
            "unhealthyPlants": [],
            "dataset": []
    }

    
    plantList = PotRegistry.objects.filter(Account=request.user)
    plantSerialIDList = []
    for plant in plantList:
        plantSerialIDList.append(plant.SerialID)
    
    # planList
    planList = FireStoreClient.GetAppliedPlanList(plantSerialIDList)
    convertedPlanList = []
    for plan in planList:
        plantName = "None"
        try:
            plantName = PotRegistry.objects.get(SerialID=plan["plantId"]).Name
        except:
            pass
        
        for schedule in plan["Plan"]["Irrigation"]["Schedules"]:
            convertedPlan = {
                "id": plan["Key"],
                "name": plan["Plan"]["Name"],
                "type": plan["Plan"]["PlantType"],
                "time": schedule["Time"],
                "target": schedule["TargetSoilHumidity"],
                "plants": [
                    {
                        "serialID": plan["plantId"],
                        "name": plantName
                    }
                ]
            }
            convertedPlanList.append(convertedPlan)
    
    now = datetime.now().time()
    before = []
    after = []

    for plan in convertedPlanList:
        try:
            plan_time = datetime.strptime(plan["time"], "%H:%M").time()
            if plan_time <= now:
                before.append(plan)
            else:
                after.append(plan)
        except ValueError:
            pass

    before.sort(key=lambda p: datetime.strptime(p["time"], "%H:%M").time())
    after.sort(key=lambda p: datetime.strptime(p["time"], "%H:%M").time())

    # unhealthyPlants
    unhealthyPlants = FireStoreClient.GetUnhealthyPlants(plantSerialIDList)

    # dataset
    dataset = FireStoreClient.GetDataSet(plantSerialIDList)

    return {
            "listPlans": {
                "before": before,
                "after": after
        },
            "unhealthyPlants": unhealthyPlants,
            "dataset": [dataset[1:]]
    }