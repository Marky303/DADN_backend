from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Import serializers
from .serializers import *

# Import functions
from .Functions.verify import *
from .Functions.response import *
from .Functions.CRUD import *



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def EditUserInfo(request):
    try:
        error = []
        
        VerifyUserInfo(request, error)
        
        if error:
            raise Exception()
        
        # If employee information is valid, save new employee information
        UpdateUserInfoCRUD(request)
        
        # Response successful code
        return ResponseSuccessful("Information edited successfully")
        
    except Exception as e:
        # Response a error code and error content        
        if str(e):
            print(str(e))
            error.append(str(e))
        print(error)
        return ResponseError(error)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserInfo(request):
    try:
        error = []
        
        serializer = UserSerializer(request.user, many=False)
        
        # Response successful code
        return ResponseObject(serializer.data)
        
    except Exception as e:
        # Response a error code and error content        
        if str(e):
            print(str(e))
            error.append(str(e))
        print(error)
        return ResponseError(error)



