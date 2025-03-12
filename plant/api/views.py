from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Import serializers
from .serializers import *

# Import functions
from .functions.verify import *
from .functions.response import *
from .functions.CRUD import *


# Manufacture/Init a new pot
# Returns pot serialID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def InitPot(request):
    try:
        error = []
        
        VerifyManufacturer(request, error)
        
        if error:
            raise Exception()

        SerialID, Key = InitPotCRUD(request)
        
        return ResponseObject({"SerialID": SerialID, "Key": Key})
        
    except Exception as e:
        # Response a error code and error content        
        if str(e):
            print(str(e))
            error.append(str(e))
        print(error)
        return ResponseError(error)

# User registering a pot
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def RegisterPot(request):
    try:
        error = []
        
        VerifyPotRegisterInfo(request, error)
        if error:
            raise Exception()
        
        pot = VerifyPotRegisterValid(request, error)
        if error:
            raise Exception()
        
        RegisterPotCRUD(request, pot)
        
        return ResponseSuccessful("Registered pot successfully")
        
    except Exception as e:
        # Response a error code and error content        
        if str(e):
            print(str(e))
            error.append(str(e))
        print(error)
        return ResponseError(error)
    
# Get all user's pots
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllPots(request):
    try:
        error = []
        
        pots = GetAllPotCRUD(request)
        
        serializer = PotRegistrySerializer(pots, many=True)
        
        return ResponseList(serializer.data, 1)
    except Exception as e:
        # Response a error code and error content        
        if str(e):
            print(str(e))
            error.append(str(e))
        print(error)
        return ResponseError(error)
    
# Create a new plan
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreatePlan(request):
    try:
        error = []
        
        VerifyPlanInformation(request, error)
        
        if error:
            raise Exception()
        
        CreatePlanCRUD(request)
        
        return ResponseSuccessful("New plan created successfully")
        
    except Exception as e:
        # Response a error code and error content        
        if str(e):
            print(str(e))
            error.append(str(e))
        print(error)
        return ResponseError(error)

# Edit an existing plan
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def EditPlan(request):
    try:
        error = []
        
        VerifyPlanOwnership(request)
        VerifyPlanInformation(request, error)
        
        if error:
            raise Exception()
        
        EditPlanCRUD(request)
        
        return ResponseSuccessful("Plan edited successfully")
        
    except Exception as e:
        # Response a error code and error content        
        if str(e):
            print(str(e))
            error.append(str(e))
        print(error)
        return ResponseError(error)

# Get a user's plans
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllPlans(request):
    try:
        error = []
        
        plans = GetAllPlansCRUD(request)
        
        serializer = PlanSerializer(plans, many=True)
        
        return ResponseList(serializer.data, 1)
    except Exception as e:
        # Response a error code and error content        
        if str(e):
            print(str(e))
            error.append(str(e))
        print(error)
        return ResponseError(error)
    
# Edit an existing plan
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def DeletePlan(request):
    try:
        error = []
        
        VerifyPlanOwnership(request)
        
        if error:
            raise Exception()
        
        DeletePlanCRUD(request)
        
        return ResponseSuccessful("Plan deleted successfully")
        
    except Exception as e:
        # Response a error code and error content        
        if str(e):
            print(str(e))
            error.append(str(e))
        print(error)
        return ResponseError(error)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ApplySettings(request):
    try:
        error = []
        
        VerifyPlanOwnership(request)
        VerifyPotOwnership(request)
        
        if error:
            raise Exception()
        
        ApplySettingsCRUD(request)
        
        return ResponseSuccessful("Settings applied successfully")
        
    except Exception as e:
        # Response a error code and error content        
        if str(e):
            print(str(e))
            error.append(str(e))
        print(error)
        return ResponseError(error)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def DisownPot(request):
    try:
        error = []
        
        potID = VerifyPotOwnershipDisown(request)
        
        if error:
            raise Exception()
        
        DisownPotCRUD(potID)
        
        return ResponseSuccessful("Disowned pot successfully")
        
    except Exception as e:
        # Response a error code and error content        
        if str(e):
            print(str(e))
            error.append(str(e))
        print(error)
        return ResponseError(error)
    
# Plant related entries
@api_view(['POST'])
def AddTemperatureEntry(request):
    try:
        error = []
        
        
        if error:
            raise Exception()
        
        AddTemperatureCRUD(request)
        
        return ResponseSuccessful("Saved temperature")
        
    except Exception as e:
        # Response a error code and error content        
        if str(e):
            print(str(e))
            error.append(str(e))
        print(error)
        return ResponseError(error)