import os
from dotenv import load_dotenv
load_dotenv()
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.conf import settings

from plant.template.PotTemplate import *

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
    
    @classmethod
    def InitPotDocuments(cls):
        db = cls._getFireStoreClient()
        
        serialID = None
        try:
            update_time, temperatureRef = db.collection(cls._plantTemperatureCollectionName).add(statTemplate)
            serialID = temperatureRef.id
            db.collection(cls._plantMoistureCollectionName).document(serialID).set(statTemplate)
            db.collection(cls._plantSoilHumidityCollectionName).document(serialID).set(statTemplate)
            db.collection(cls._plantLightCollectionName).document(serialID).set(statTemplate)
            db.collection(cls._plantNotificationsCollectionName).document(serialID).set(notificationsTemplate)
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
    
    # TODO: Implement Notify function
    @classmethod
    def Notify(cls, serialID, type, message):
        db = cls._getFireStoreClient()
        db.collection(cls._plantNotificationsCollectionName).document(serialID)

    