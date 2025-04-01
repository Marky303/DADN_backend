import os
from dotenv import load_dotenv
load_dotenv()
from django.conf import settings
import datetime

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

GetAllPots = {
    "name": "get_all_user_pots",
    "description": "Get a list of the user's registered pots"
}

# Gemini properties declarations
declaredFunctionPrototypes = [RegisterPlanFunction, GetAllPots]

instructionFilePath     = str(settings.BASE_DIR) + "/assistant/gemini/templates/SystemInstructions.txt"
instructionFile         = open(instructionFilePath) 
instruction             = instructionFile.read()

# Adding system information
instruction = instruction.replace("<time>", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

modelName               = os.getenv("GEMINI_MODEL_NAME")

apiKey                  = os.getenv("GEMINI_API_KEY")