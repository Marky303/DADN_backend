from datetime import datetime

notificationTempate = {
                            "id": "1",
                            "Time": datetime.now().timestamp(),
                            "Type": "info",
                            "Content": "Pot is manufactured",
                            "Seen": False
                    }

notificationsTemplate = {
                            "Key": "",
                            "Logs": [
                                    notificationTempate
                                ]
                        }

statTemplate = {
                    "Logs": [
                                {"Time": datetime.now().timestamp(), "Value": 0}
                            ]
                }

planDataTemplate = {
                        "Name": "Cactus Plan",
                        "PlantType": "Cactus",
                        "StatRanges": {
                            "Temperature": {
                                "min": 20,
                                "max": 35
                            },
                            "Moisture": {
                                "min": 20,
                                "max": 35
                            },
                            "SoilHumidity": {
                                "min": 20,
                                "max": 35
                            },
                            "Light": {
                                "min": 20,
                                "max": 35
                            }
                        },
                        "Irrigation": {
                            "Schedules": [
                                { "Time": "06:00", "TargetSoilHumidity": 50 },
                            ],
                            "Conditions": [
                                { 
                                    "TargetStat": "SoilHumidity", 
                                    "TargetValue": 30, 
                                    "TargetSoilHumidity": 50, 
                                    "Type": ">",
                                    "Cooldown": 7200
                                },
                            ]
                        }
                    }

planTemplate = {
                    "Key": "",
                    "Plan": planDataTemplate,
                }

verifyTemplate = {
    "Key": ""
}