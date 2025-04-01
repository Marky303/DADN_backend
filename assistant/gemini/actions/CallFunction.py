from assistant.api.functions.verify import *
from assistant.api.functions.CRUD import *

def callFunction(part, request):
    functionCall = part["function_call"]
    result = None
    
    # Function cases___________________________________________
    if functionCall["name"] == "register_pot":
        result = register_pot(request, **functionCall["args"])
        
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

def register_pot(request, serialID, key):
    try:
        VerifyPotRegisterInfo(serialID, key)
        pot = VerifyPotRegisterValid(serialID, key)
        RegisterPotCRUD(request, pot)
        return {"detail": "Successfully registered pot" + serialID}
    except Exception as e:
        return {"detail": str(e)}