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
        query, documentID = getParamsFromRequest(request)
        
        # Create new document
        if documentID is None:
            documentID, history = FireStoreClient.createChatDocument()
        else:
            history = FireStoreClient.getChatHistory(documentID)
            
        # Progress chat history
        chat = GeminiController(query, history, request)
        
        # Save the new chat history
        FireStoreClient.saveChatHistory(chat, documentID)

        return ResponseObject({"documentID": documentID})
          
    except Exception as e:
        return errorHandling(e)    

# Helper functions
def getParamsFromRequest(request):
    requestBodyUnicode  = request.body.decode("UTF-8")
    requestDictionary   = json.loads(requestBodyUnicode)
    query               = requestDictionary['query']
    try:
        documentID      = requestDictionary['documentID']
    except Exception as e:
        documentID      = None
    return query, documentID

def errorHandling(e):
    return ResponseError(str(e)) 





# API for testing
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def TEST(request):
    try:
        error = []
        query, documentID = getParamsFromRequest(request)
        if error:
            raise Exception()
        
        # TEST HERE
        chat = GeminiController(query, [], request)
        
        return ResponseObject(chat)
          
    except Exception as e:
        return errorHandling(e)