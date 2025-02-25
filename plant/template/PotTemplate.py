from datetime import datetime

notificationTempate = {
                            "id": "1",
                            "Time": datetime.now().timestamp(),
                            "Type": "info",
                            "Content": "Pot is manufactured",
                            "Seen": False
                    }

notificationsTemplate = {
                            "Log": [
                                    notificationTempate
                                ]
                        }

statTemplate = {
                    "Log": [
                                {"Time": datetime.now().timestamp(), "Value": 0}
                            ]
                }

planTemplate = {
                    "plan": None
                }