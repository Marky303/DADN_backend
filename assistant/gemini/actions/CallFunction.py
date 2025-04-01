from assistant.api.functions.verify import *
from assistant.api.functions.CRUD import *

from plant.api.functions.verify import *
from plant.api.functions.CRUD import *

from plant.api.serializers import *

# Controller
def callFunction(part, request):
    functionCall = part["function_call"]
    result = None
    
    # Function cases___________________________________________
    if functionCall["name"] == "register_pot":
        result = register_pot(request, **functionCall["args"])
        
    if functionCall["name"] == "get_all_user_pots":
        result = get_all_user_pots(request)
        
    # Template
    if functionCall["name"] == "something_function":
        result = None
        
    # End of function cases____________________________________
    
    if result is not None:
        functionResponseTemplate = {
            "name": functionCall["name"],
            "response": result
        }
        return functionResponseTemplate
    return None

# Actual functions
def register_pot(request, serialID, key):
    try:
        VerifyPotRegisterInfo(serialID, key)
        pot = VerifyPotRegisterValid(serialID, key)
        RegisterPotCRUD(request, pot)
        return {"detail": "Successfully registered pot" + serialID}
    except Exception as e:
        return errorHandling(e)
    
def get_all_user_pots(request):
    try:
        pots = GetAllPotCRUD(request)
        serializer = PotRegistrySerializer(pots, many=True)
        return {"list": serializer.data}
    except Exception as e:
        return errorHandling(e)
    
# Error handling
def errorHandling(e):
    return {"error": str(e)}