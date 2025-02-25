import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.conf import settings

class FireStoreClient:
    _db = None
    
    _plantTemperatureCollectionName     = os.getenv("FIRESTORE_PLANT_TEMPERATURE_COLLECTION")
    _plantMoistureCollectionName        = os.getenv("FIRESTORE_PLANT_MOISTURE_COLLECTION")
    _plantSoilHumidityCollectionName    = os.getenv("FIRESTORE_PLANT_SOILHUMIDITY_COLLECTION")
    _plantLightCollectionName           = os.getenv("FIRESTORE_PLANT_LIGHT_COLLECTION")
    _plantNotificationsCollectionName   = os.getenv("FIRESTORE_PLANT_NOTIFICATIONS_COLLECTION")
    _plantPlanCollectionName            = os.getenv("FIRESTORE_PLANT_PLAN_COLLECTION")
    
    @classmethod
    def _getFireStoreClient(cls):
        if cls._db is None:
            cred = credentials.Certificate(str(settings.BASE_DIR) + "\\firebase_key.json")
            firebase_admin.initialize_app(cred)
            cls._db = firestore.client()
        return cls._db
    
    # TODO: Save templates somewhere then import
    @classmethod
    def InitPotDocuments(cls):
        db = cls._getFireStoreClient()
        
        timestampNow = datetime.now().timestamp()
        statTemplate = {"Log": [{"Time": timestampNow, "Value": 0}]}
        
        serialID = None
        try:
            update_time, temperatureRef = db.collection(cls._plantTemperatureCollectionName).add(statTemplate)
            serialID = temperatureRef.id
            
            db.collection(cls._plantMoistureCollectionName).document(serialID).set(statTemplate)
            db.collection(cls._plantSoilHumidityCollectionName).document(serialID).set(statTemplate)
            db.collection(cls._plantLightCollectionName).document(serialID).set(statTemplate)
            
            notificationsTemplate = {
                                        "Log": [
                                                {
                                                    "id": "1",
                                                    "Time": timestampNow,
                                                    "Type": "info",
                                                    "Content": "Pot is manufactured",
                                                    "Seen": False
                                                }
                                            ]
                                    }
            db.collection(cls._plantNotificationsCollectionName).document(serialID).set(notificationsTemplate)
            
            planTemplate = {"plan": None}
            db.collection(cls._plantPlanCollectionName).document(serialID).set(planTemplate)
            
        except Exception as e:
            if serialID is not None:
                db.collection(cls._plantTemperatureCollectionName)  .document(serialID).delete()
                db.collection(cls._plantMoistureCollectionName)     .document(serialID).delete()
                db.collection(cls._plantSoilHumidityCollectionName) .document(serialID).delete()
                db.collection(cls._plantLightCollectionName)        .document(serialID).delete()
                db.collection(cls._plantNotificationsCollectionName).document(serialID).delete()
                db.collection(cls._plantPlanCollectionName)         .document(serialID).delete()
            
        return serialID
    
    # @classmethod
    # def UpdateChatHistoryDocument(cls, documentID, chatHistory):
    #     db = cls._getFireStoreClient()
    #     db.collection(cls._historyCollectionName).document(documentID).set(chatHistory)

    