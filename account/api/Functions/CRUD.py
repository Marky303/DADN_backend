import json

# Import models
from account.models import *

def UpdateUserInfoCRUD(request):
    dict = request.body.decode("UTF-8")
    userInfo = json.loads(dict)
    
    currentUser = request.user
    
    currentUser.Name        = userInfo["Name"]
    currentUser.PhoneNumber = userInfo["PhoneNumber"]
    currentUser.DateOfBirth = userInfo["DateOfBirth"]
    currentUser.Gender      = userInfo["Gender"]
    currentUser.Address     = userInfo["Address"]
    currentUser.Avatar      = userInfo["Avatar"]
    
    currentUser.save()
    
def GetUserInfoCRUD(request):
    return request.user
    
    