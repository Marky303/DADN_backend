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