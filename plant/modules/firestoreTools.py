import os
from dotenv import load_dotenv
load_dotenv()
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.conf import settings
import json

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
    
    @staticmethod
    def CreateLogSubCollection(ref):
        logsCollectionRef = ref.collection(f"Logs")
        logsCollectionRef.add({
            "Time": datetime.now().timestamp(),
            "Value": 0
        })
    
    @classmethod
    def InitPotDocuments(cls, Key):
        db = cls._getFireStoreClient()
        
        serialID = None
        try:
            verifyTemplate["Key"] = Key
            
            update_time, temperatureRef = db.collection(cls._plantTemperatureCollectionName).add(verifyTemplate)
            cls.CreateLogSubCollection(temperatureRef)
            serialID = temperatureRef.id
            
            moistureRef = db.collection(cls._plantMoistureCollectionName).document(serialID)
            moistureRef.set(verifyTemplate)
            cls.CreateLogSubCollection(moistureRef)

            soilHumidityRef = db.collection(cls._plantSoilHumidityCollectionName).document(serialID)
            soilHumidityRef.set(verifyTemplate)
            cls.CreateLogSubCollection(soilHumidityRef)

            lightRef = db.collection(cls._plantLightCollectionName).document(serialID)
            lightRef.set(verifyTemplate)
            cls.CreateLogSubCollection(lightRef)
            
            notificationsTemplate["Key"] = Key
            db.collection(cls._plantNotificationsCollectionName).document(serialID).set(notificationsTemplate)
            
            planTemplate["Key"] = Key
            db.collection(cls._plantPlanCollectionName).document(serialID).set(planTemplate)
            
        except Exception as e:
            if serialID is not None:
                cls.forceDeleteDocument(db.collection(cls._plantTemperatureCollectionName)  .document(serialID))
                cls.forceDeleteDocument(db.collection(cls._plantMoistureCollectionName)     .document(serialID))
                cls.forceDeleteDocument(db.collection(cls._plantSoilHumidityCollectionName) .document(serialID))
                cls.forceDeleteDocument(db.collection(cls._plantLightCollectionName)        .document(serialID))
                cls.forceDeleteDocument(db.collection(cls._plantNotificationsCollectionName).document(serialID))
                cls.forceDeleteDocument(db.collection(cls._plantPlanCollectionName)         .document(serialID))
            
        return serialID
    
    @staticmethod
    def GetNextNotificationId(notificationRef):
        doc = notificationRef.get()
        if doc.exists:
            currentLog = doc.to_dict().get("Logs", [])
            print(currentLog)
            nextID = str(len(currentLog) + 1)
        return nextID
    
    @classmethod
    def Notify(cls, serialID, content, type="info"):
        db = cls._getFireStoreClient()
        notificationRef = db.collection(cls._plantNotificationsCollectionName).document(serialID)
        
        notification = notificationTempate
        notification["Type"] = type
        notification["Content"] = content
        notification["id"] = cls.GetNextNotificationId(notificationRef)  
        
        notificationRef.update({
            "Logs": firestore.ArrayUnion([notification])
        })

    # ADMIN FUNCTIONS
    @classmethod
    def initFirestoreDatabase(cls):
        db = cls._getFireStoreClient()
        collections = [
            cls._plantTemperatureCollectionName,
            cls._plantMoistureCollectionName,
            cls._plantSoilHumidityCollectionName,
            cls._plantLightCollectionName,
            cls._plantNotificationsCollectionName,
            cls._plantPlanCollectionName
        ]
        for collection in collections:
            doc_ref = db.collection(collection).document("anchor")
            doc_ref.set({"content": 0})
        print("Migrated nosql database")
    
    @staticmethod
    def forceDeleteDocument(docRef):
        try:
            subcollections = list(docRef.collections())  
            for subcollection in subcollections:
                FireStoreClient.forceDeleteCollection(subcollection)  
            docRef.delete()
        except Exception as e:
            print(f'Failed to delete {docRef.id}: {e}')

    @staticmethod
    def forceDeleteCollection(colRef):
        try:
            docs = list(colRef.stream())
            for doc in docs:
                FireStoreClient.forceDeleteDocument(doc.reference)
        except Exception as e:
            print(f'Failed to delete collection {colRef.id}: {e}')
    
    @classmethod
    def nuke(cls):
        db = cls._getFireStoreClient()
        collections = db.collections()
        for col in collections:
            print(f'Nuking collection: {col.id}')
            cls.forceDeleteCollection(col)
        print("Nuked everything")
                    
    @classmethod
    def ApplyPlan(cls, serialID, JSON, Key):
        db = cls._getFireStoreClient()

        planTemplate['Key'] = Key
        planTemplate['Plan'] = json.loads(JSON)
        
        db.collection(cls._plantPlanCollectionName).document(serialID).set(planTemplate)
        
    @classmethod
    def addTemperatureEntry(cls, entry, serialID):        
        db = cls._getFireStoreClient()
        
        db.collection(cls._plantTemperatureCollectionName).document(serialID).collection('Logs').add(entry)