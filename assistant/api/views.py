from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json

from plant.modules.firestoreTools import FireStoreClient
from assistant.gemini.GeminiController import GeminiController

# Import serializers
from .serializers import *

# Import functions
from .functions.verify import *
from .functions.response import *
from .functions.CRUD import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Chat(request):
    try:
        error = []
        query = getUserQueryFromRequest(request)
        if error:
            raise Exception()
        
        # Create new document
        documentID, history = FireStoreClient.createChatDocument()
        
        # Progress chat history
        chat = GeminiController(query, history)
        
        # Save the new chat history
        FireStoreClient.saveChatHistory(chat, documentID)
        
        return ResponseObject({"documentID": documentID})
          
    except Exception as exception:
        return errorHandling(exception, error)    

# Helper functions
def getUserQueryFromRequest(request):
    requestBodyUnicode  = request.body.decode("UTF-8")
    requestDictionary   = json.loads(requestBodyUnicode)
    userQuery           = requestDictionary['query']
    return userQuery

def errorHandling(exception, error):
    if str(exception): error.append(str(exception))
    return ResponseError(error) 



# API for testing
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def TEST(request):
    try:
        error = []
        query = getUserQueryFromRequest(request)
        if error:
            raise Exception()
        
        # TEST HERE
        chat = GeminiController(query, [], request)
        
        return ResponseObject(chat)
          
    except Exception as exception:
        return errorHandling(exception, error)  