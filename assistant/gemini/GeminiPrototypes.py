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

CreatePlan = {
    "name": "create_plan",
    "description": """Create a plan to manage the pot automatically. Walk the user through creating a plan.""",
    "parameters": {
        "type": "object",
        "properties": {
            "plan": {
                "type": "object",
                "description": "Plan object parameter",
                "properties": {
                    "Name": {
                        "type": "string",
                        "description": "This is the identifier or title given to the specific plant care plan."
                    },
                    "PlantType": {
                        "type": "string",
                        "description": "This indicates the kind of plant that this care plan is designed for (e.g., Cactus)."
                    },
                    "StatRanges": {
                        "type": "object",
                        "description": "Defines the desired ranges for various environmental conditions. Notifications will be sent if any value is outside the ideal range.",
                        "properties": {
                            "Temperature": {
                                "type": "object",
                                "description": "Specifies the minimum and maximum acceptable temperature for the plant.",
                                "properties": {
                                    "min": {"type": "number", "description": "Minimum acceptable temperature."},
                                    "max": {"type": "number", "description": "Maximum acceptable temperature."}
                                },
                                "required": ["min", "max"]
                            },
                            "Moisture": {
                                "type": "object",
                                "description": "Specifies the minimum and maximum desired moisture levels.",
                                "properties": {
                                    "min": {"type": "number", "description": "Minimum desired moisture level."},
                                    "max": {"type": "number", "description": "Maximum desired moisture level."}
                                },
                                "required": ["min", "max"]
                            },
                            "SoilHumidity": {
                                "type": "object",
                                "description": "Specifies the minimum and maximum desired humidity levels in the soil.",
                                "properties": {
                                    "min": {"type": "number", "description": "Minimum desired soil humidity."},
                                    "max": {"type": "number", "description": "Maximum desired soil humidity."}
                                },
                                "required": ["min", "max"]
                            },
                            "Light": {
                                "type": "object",
                                "description": "Specifies the minimum and maximum desired light intensity for the plant.",
                                "properties": {
                                    "min": {"type": "number", "description": "Minimum desired light level."},
                                    "max": {"type": "number", "description": "Maximum desired light level."}
                                },
                                "required": ["min", "max"]
                            }
                        },
                        "required": ["Temperature", "Moisture", "SoilHumidity", "Light"]
                    },
                    "Irrigation": {
                        "type": "object",
                        "description": "Details the automated watering schedule and conditions for the plant.",
                        "properties": {
                            "Schedules": {
                                "type": "array",
                                "description": "A list of specific times during the day to water the plant and the target soil humidity level after watering.",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "Time": {
                                            "type": "string",
                                            "pattern": "^(?:[01]\\d|2[0-3]):[0-5]\\d$",
                                            "description": "The time in the day to water the plant (e.g., 06:00)."
                                        },
                                        "TargetSoilHumidity": {
                                            "type": "number",
                                            "description": "The soil humidity level to reach after watering is triggered by this schedule."
                                        }
                                    },
                                    "required": ["Time", "TargetSoilHumidity"]
                                }
                            },
                            "Conditions": {
                                "type": "array",
                                "description": "Rules that trigger automatic watering based on current environmental conditions.",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "TargetStat": {
                                            "type": "string",
                                            "enum": ["Temperature", "Moisture", "SoilHumidity", "Light"],
                                            "description": "The specific plant metric being monitored (e.g., SoilHumidity)."
                                        },
                                        "Type": {
                                            "type": "string",
                                            "enum": [">", "<"],
                                            "description": "The comparison operator to use (e.g., '>', '<')."
                                        },
                                        "TargetValue": {
                                            "type": "number",
                                            "description": "The threshold value that triggers watering when exceeded or not met."
                                        },
                                        "TargetSoilHumidity": {
                                            "type": "number",
                                            "description": "The soil humidity level to reach after this condition triggers watering."
                                        },
                                        "Cooldown": {
                                            "type": "number",
                                            "description": "A cooldown period in seconds after a condition is triggered, during which it can't be triggered again."
                                        }
                                    },
                                    "required": ["TargetStat", "TargetValue", "TargetSoilHumidity"]
                                }
                            }
                        },
                        "required": ["Schedules", "Conditions"]
                    }
                },
                "required": ["Name", "PlantType", "StatRanges", "Irrigation"]
            }
        },
        "required": ["plan"]
    }
}

FindUserPlans = {
    "name": "find_user_plans",
    "description": 
        """Get a list of the user's plans based on the specified filters. If no filter is included, this query will return all user's plans.
        This function will return a list of user's plans with 3 properties: id of the plan in the database, Name of the plan and the JSON content of the plan.""",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name filter of the query. This filter is not case sensitive and will find plans based on substring matches. If passed an empty string, this filter will not be included in the query.",
            }
        },
        "required": ["name"],
    }
}

# Gemini properties declarations
declaredFunctionPrototypes = [RegisterPlanFunction, FindUserPots, GetPotStatus, CreatePlan, FindUserPlans]

instructionFilePath     = str(settings.BASE_DIR) + "/assistant/gemini/templates/SystemInstructions.txt"
instructionFile         = open(instructionFilePath) 
instruction             = instructionFile.read()

# Adding system information
instruction = instruction.replace("<time>", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

modelName               = os.getenv("GEMINI_MODEL_NAME")

apiKey                  = os.getenv("GEMINI_API_KEY")