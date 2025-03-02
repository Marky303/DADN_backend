from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Import serializers
from .serializers import *

# Import functions
from .Functions.verify import *
from .Functions.response import *
from .Functions.CRUD import *


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