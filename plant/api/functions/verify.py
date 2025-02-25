import json
import jsonschema
from jsonschema import validate

from plant.models import *

def VerifyManufacturer(request, error):
    user = request.user
    if not user.is_manufacturer:
        error.append("Only manufacturer can init a plant")
    
# TODO: Complete this
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
    
# TODO: Implement this    
def VerifyPotRegisterValid(request, error):
    dict = request.body.decode("UTF-8")
    registerInfo = json.loads(dict)
    
    try:
        pot = PotRegistry.objects.get(SerialID=registerInfo["SerialID"])
    except Exception as e:
        error.append("Invalid pot information")
        return
    
    if pot.Account is not None:
        error.append("Pot has already been registered")
        return
    
    return pot
    