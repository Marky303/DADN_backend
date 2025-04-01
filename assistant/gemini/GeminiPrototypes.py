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

FindUserPots = {
    "name": "find_user_pots",
    "description": "Get a list of the user's registered pots based on the specified filters. If no filter is included, this query will return all user's pots",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name filter of the query. This filter is not case sensitive and will find pots based on substring matches. If passed an empty string, this filter will not be included in the query.",
            },
            "serialID": {
                "type": "string",
                "description": "The serialID filter of the query. This filter must be 100% match. If passed an empty string, this filter will not be included in the query.",
            },
        },
        "required": ["name", "serialID"],
    }
}

GetPotStatus = {
    "name": "get_pot_status",
    "description": 
    """Get the current status (Temperature, Light, Moisture, Soil humidity), notification list and the pot's settings (name and applied plan) of the pot.
        When user specify the name of a pot, always use the get_all_user_pots function to query for the pot serial ID and use that as parameter for this function.""",
    "parameters": {
        "type": "object",
        "properties": {
            "serialID": {
                "type": "string",
                "description": "Serial ID of the smart pot product. Every serial ID follows this regex pattern ^[A-Za-z0-9]{20}$",
            },
        },
        "required": ["serialID"],
    }
}

# Gemini properties declarations
declaredFunctionPrototypes = [RegisterPlanFunction, FindUserPots, GetPotStatus]

instructionFilePath     = str(settings.BASE_DIR) + "/assistant/gemini/templates/SystemInstructions.txt"
instructionFile         = open(instructionFilePath) 
instruction             = instructionFile.read()

# Adding system information
instruction = instruction.replace("<time>", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

modelName               = os.getenv("GEMINI_MODEL_NAME")

apiKey                  = os.getenv("GEMINI_API_KEY")