import json
import jsonschema
from jsonschema import validate

# Import models
from account.models import *

def VerifyUserInfo(request, error):
    dict = request.body.decode("UTF-8")
    userInfo = json.loads(dict)
    
    userInfoSchema = {
    "type": "object",
    "properties": {
        "Name":         {"type": "string", "maxLength": 50},
        "PhoneNumber":  {"type": "string", "maxLength": 20},
        "DateOfBirth":  {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
        "Gender":       {"type": "string", "enum": ["F", "M"]},
        "Address":      {"type": "string", "maxLength": 50}
        },
    "required": ["Name", "PhoneNumber", "DateOfBirth", "Gender", "Address"]
    }   
    
    try:
        validate(instance=userInfo, schema=userInfoSchema)
    except jsonschema.exceptions.ValidationError as e:
        error.append(e.message)