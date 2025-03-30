import json
import jsonschema
from jsonschema import validate

from plant.models import *

def VerifyManufacturer(request, error):
    user = request.user
    if not user.is_manufacturer:
        error.append("Only manufacturer can init a plant")
    
def VerifyPotRegisterInfo(request, error):
    dict = request.body.decode("UTF-8")
    registerInfo = json.loads(dict)
    
    registerInfoSchema = {
        "type": "object",
        "properties": {
            "SerialID":     {"type": "string", "pattern": "^[A-Za-z0-9]{20}$"},
            "Key":          {"type": "string", "pattern": "^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$"},
        },
        "required": ["SerialID", "Key"]
    }   
    
    try:
        validate(instance=registerInfo, schema=registerInfoSchema)
    except jsonschema.exceptions.ValidationError as e:
        error.append(e.message)
      
def VerifyPotRegisterValid(request, error):
    dict = request.body.decode("UTF-8")
    registerInfo = json.loads(dict)
    
    try:
        pot = PotRegistry.objects.get(SerialID=registerInfo["SerialID"])
    except Exception as e:
        error.append("Invalid pot information")
        return
    
    if pot.Key != registerInfo['Key']:
        error.append("Invalid pot information")
        return
    
    if pot.Account is not None:
        error.append("Pot has already been registered")
        return
    
    return pot

def VerifyPlanOwnership(request):
    dict = request.body.decode("UTF-8")
    planInfo = json.loads(dict)
    
    planID = planInfo["planID"]
    plan = Plan.objects.get(id=planID)
    if plan.Account != request.user:
        raise Exception("This plan is not yours")
    
def VerifyPotOwnership(request):
    dict = request.body.decode("UTF-8")
    potInfo = json.loads(dict)
    
    potID = potInfo['potID']
    pot = PotRegistry.objects.get(id=potID)
    if pot.Account != request.user:
        raise Exception("This pot is not yours")
    
def VerifyPotOwnershipDisown(request):
    dict = request.body.decode("UTF-8")
    potInfo = json.loads(dict)
    
    serialID = potInfo['serialID']
    pot = PotRegistry.objects.get(SerialID=serialID)
    if pot.Account != request.user:
        raise Exception("This pot is not yours")
    return pot.id

def VerifyPlanInformation(request, error):
    dict = request.body.decode("UTF-8")
    planInfo = json.loads(dict)
    
    planInfoSchema = {
        "type": "object",
        "properties": {
            "Name": {"type": "string"},
            "PlantType": {"type": "string"},
            "StatRanges": {
                "type": "object",
                "properties": {
                    "Temperature": {
                        "type": "object",
                        "properties": {
                            "min": {"type": "number"},
                            "max": {"type": "number"}
                        },
                        "required": ["min", "max"]
                    },
                    "Moisture": {
                        "type": "object",
                        "properties": {
                            "min": {"type": "number"},
                            "max": {"type": "number"}
                        },
                        "required": ["min", "max"]
                    },
                    "SoilHumidity": {
                        "type": "object",
                        "properties": {
                            "min": {"type": "number"},
                            "max": {"type": "number"}
                        },
                        "required": ["min", "max"]
                    },
                    "Light": {
                        "type": "object",
                        "properties": {
                            "min": {"type": "number"},
                            "max": {"type": "number"}
                        },
                        "required": ["min", "max"]
                    }
                },
                "required": ["Temperature", "Moisture", "SoilHumidity", "Light"]
            },
            "Irrigation": {
                "type": "object",
                "properties": {
                    "Schedules": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "Time": {"type": "string", "pattern": "^(?:[01]\\d|2[0-3]):[0-5]\\d$"},
                                "TargetSoilHumidity": {"type": "number"}
                            },
                            "required": ["Time", "TargetSoilHumidity"]
                        }
                    },
                    "Conditions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "TargetStat": {
                                    "type": "string",
                                    "enum": ["Temperature", "Moisture", "SoilHumidity", "Light"]
                                },
                                "Type": {
                                    "type": "string",
                                    "enum": [">", "<"]
                                },
                                "TargetValue": {"type": "number"},
                                "TargetSoilHumidity": {"type": "number"},
                                "Cooldown": {"type": "number"}
                            },
                            "required": ["TargetStat", "TargetValue", "TargetSoilHumidity"]
                        }
                    }
                },
                "required": ["Schedules", "Conditions"]
            }
        },
        "required": ["Name", "PlantType", "StatRanges", "Irrigation"]
    }
   
    
    try:
        validate(instance=planInfo, schema=planInfoSchema)
    except jsonschema.exceptions.ValidationError as e:
        error.append(e.message)
    