import json
import jsonschema
from jsonschema import validate
import re

from plant.models import *
    
def VerifyPotRegisterInfo(serialID, key):
    key_regex = r"^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$"
    serialID_regex = r"^[A-Za-z0-9]{20}$"

    if not re.match(key_regex, key):
        raise Exception("Invalid key format")

    if not re.match(serialID_regex, serialID):
        raise Exception("Invalid serialID format")

def VerifyPotRegisterValid(serialID, key):
    try:
        pot = PotRegistry.objects.get(SerialID=serialID)
    except Exception as e:
        raise Exception("Cannot find pot")
    
    if pot.Key != key:
        raise Exception("Invalid pot information")
    
    if pot.Account is not None:
        raise Exception("Pot has already been registered")
    
    return pot

def VerifyPotOwnership(request, serialID):
    try:
        pot = PotRegistry.objects.get(SerialID=serialID)
    except Exception as e:
        raise Exception("Cannot find pot")
    
    if pot.Account != request.user:
        raise Exception("This pot is not yours")
    
def VerifyPlanInformation(plan):
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
        validate(instance=plan, schema=planInfoSchema)
    except jsonschema.exceptions.ValidationError as e:
        raise e