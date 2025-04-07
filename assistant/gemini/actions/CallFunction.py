from plant.api.functions.verify import *
from plant.api.functions.CRUD import *

from assistant.api.functions.verify import *
from assistant.api.functions.CRUD import *

from plant.api.serializers import *

from plant.modules.firestoreTools import FireStoreClient

# Controller
def callFunction(part, request):
    functionCall = part["function_call"]
    result = None
    
    # Function cases___________________________________________
    if functionCall["name"] == "register_pot":
        result = register_pot(request, **functionCall["args"])
        
    if functionCall["name"] == "find_user_pots":
        result = find_user_pots(request, **functionCall["args"])
        
    if functionCall["name"] == "get_pot_status":
        result = get_pot_status(request, **functionCall["args"])    
        
    if functionCall["name"] == "create_plan":
        result = create_plan(request, **functionCall["args"]) 
        
    if functionCall["name"] == "find_user_plans":
        result = find_user_plans(request, **functionCall["args"]) 
    
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
    
def find_user_pots(request, name, serialID):
    try:
        pots = FindPotsCRUD(request, name, serialID)
        serializer = PotRegistrySerializer(pots, many=True)
        return {"list": serializer.data}
    except Exception as e:
        return errorHandling(e)
    
def get_pot_status(request, serialID):
    try:
        VerifyPotOwnership(request, serialID)
        return FireStoreClient.getPotStatus(serialID)
    except Exception as e:
        return errorHandling(e)
    
def create_plan(request, plan):
    try:
        VerifyPlanInformation(plan)
        CreatePlanCRUD(request, plan)        
        return {"detail": "Successfully created plan"}
    except Exception as e:    
        return errorHandling(e)

def find_user_plans(request, name):
    try:
        plans = FindPlansCRUD(request, name)
        serializer = PlanSerializer(plans, many=True)
        return {"list": serializer.data}
    except Exception as e:    
        return errorHandling(e)

# Error handling
def errorHandling(e):
    return {"error": str(e)}