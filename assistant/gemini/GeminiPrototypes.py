import os
from dotenv import load_dotenv
load_dotenv()
from django.conf import settings
from typing import List

# Function declarations prototypes
RegisterPlanFunction = {
    "name": "register_pot",
    "description": "Register a smart pot for the user using the provided serial ID and key",
    "parameters": {
        "type": "object",
        "properties": {
            "serialID": {
                "type": "string",
                "description": "Serial ID of the smart pot product. Every serial ID follows this regex pattern ^[A-Za-z0-9]{20}$",
            },
            "key": {
                "type": "string",
                "description": "Key of the smart pot product. Every key follows this regex pattern ^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$",
            },
        },
        "required": ["serialID", "key"],
    }
}


# Gemini properties declarations
declaredFunctionPrototypes = [RegisterPlanFunction]

instructionFilePath     = str(settings.BASE_DIR) + "/assistant/gemini/templates/SystemInstructions.txt"
instructionFile         = open(instructionFilePath) 
instruction             = instructionFile.read()

modelName               = os.getenv("GEMINI_MODEL_NAME")

apiKey                  = os.getenv("GEMINI_API_KEY")

# Notice: Mock search function can be inserted here
def callFunction(modelResponse, ):
    functionResponseTemplates = []
    for part in modelResponse.parts:
        if fn := part.function_call:
            params = fn.args
            functionResponseTemplate = {
                "name"  : fn.name,
                "result": None
            }
            
            if      fn.name == "SearchUsingEverySearchEngine":
                # functionResponseTemplate["result"] = GlobalMockSearch(params["keyword"], int(params["precedentSearchID"]))
                pass
                
            elif    fn.name == "SpecificGoogleNewsSearch":          
                # functionResponseTemplate["result"] = GoogleNewsMockSearch(params["keyword"], int(params["precedentSearchID"]))
                pass
                
            elif    fn.name == "SpecificFacebookPostSearch":    
                # functionResponseTemplate["result"] = FacebookPostSearch(params["keyword"], int(params["precedentSearchID"]))
                pass
                
            elif    fn.name == "SpecificYoutubeVideoSearch":    
                # functionResponseTemplate["result"] = YoutubeVideoMockSearch(params["keyword"], int(params["precedentSearchID"]))
                pass
                
            functionResponseTemplates.append(functionResponseTemplate)
        
    return functionResponseTemplates

    
    