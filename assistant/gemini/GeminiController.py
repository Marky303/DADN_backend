from google import genai
from google.genai import types

from assistant.gemini.GeminiPrototypes import apiKey, modelName, instruction, declaredFunctionPrototypes
from assistant.gemini.actions.CallFunction import callFunction

def GeminiController(query, history, request):
    chat        = initChatInterface(history)
    tokenCount  = 0
    
    try:
        modelResponse = chat.send_message(query) 
        
        while True:
            tokenCount          = modelResponse.usage_metadata.total_token_count
            responseParts       = modelResponse.candidates[0].content.to_json_dict()['parts']

            userTurnParts       = []
            for part in responseParts:
                result          = handlePart(part, request)
                if result is not None: userTurnParts.append(result)

            if len(userTurnParts) == 0:
                break

            modelResponse       = chat.send_message(userTurnParts) 
            
        newHistoryObjs          = chat.get_history()
        newHistory              = list(map(lambda obj: obj.to_json_dict(), newHistoryObjs))
        chat = {
            "Token": tokenCount,
            "History": newHistory
        }
        return chat
    except Exception as e:
        print(e)
        raise e
    
# Helper function
def loadHistory(history):
    return history

def initChatInterface(history):
    tools   = types.Tool(function_declarations=declaredFunctionPrototypes)
    config  = types.GenerateContentConfig(tools=[tools],
                                         system_instruction=instruction)
    client  = genai.Client(api_key=apiKey)
    chat    = client.chats.create(model=modelName, 
                                  config=config, 
                                  history=history)
    return chat

# Handle each part type
def handlePart(part, request):
    if "function_call" in part.keys():
        functionResponse = callFunction(part, request)
        return types.Part(function_response=functionResponse)
    return None