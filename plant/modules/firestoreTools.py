import os
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict
load_dotenv()
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.conf import settings
import json

from plant.models import *

from plant.template.PotTemplate import *

class FireStoreClient:
    _db = None
    
    # Plant related
    _plantTemperatureCollectionName     = os.getenv("FIRESTORE_PLANT_TEMPERATURE_COLLECTION")
    _plantMoistureCollectionName        = os.getenv("FIRESTORE_PLANT_MOISTURE_COLLECTION")
    _plantSoilHumidityCollectionName    = os.getenv("FIRESTORE_PLANT_SOILHUMIDITY_COLLECTION")
    _plantLightCollectionName           = os.getenv("FIRESTORE_PLANT_LIGHT_COLLECTION")
    _plantNotificationsCollectionName   = os.getenv("FIRESTORE_PLANT_NOTIFICATIONS_COLLECTION")
    _plantPlanCollectionName            = os.getenv("FIRESTORE_PLANT_PLAN_COLLECTION")
    
    @classmethod
    def _getFireStoreClient(cls):
        if cls._db is None:
            cred = credentials.Certificate(str(settings.BASE_DIR) + "/firebase_key.json")
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
        
    @classmethod
    def GetAppliedPlanList(cls, serialIDList):
        db = cls._getFireStoreClient()
        
        planList = []
        
        for serialID in serialIDList:
            planRef = db.collection(cls._plantPlanCollectionName).document(serialID)
            doc = planRef.get()
            if doc.exists:
                plan = doc.to_dict()
                plan["plantId"] = doc.id
                planList.append(plan)

        return planList
    
    @classmethod
    def GetUnhealthyPlants(cls, serialIDList):
        db = cls._getFireStoreClient()
        plantList = []

        for serialID in serialIDList:
            planRef = db.collection(cls._plantPlanCollectionName).document(serialID)
            doc = planRef.get()
            if not doc.exists:
                continue

            plan = doc.to_dict()
            statRanges = plan['Plan']['StatRanges']
            name = PotRegistry.objects.get(SerialID=doc.id).Name

            # Get latest sensor values
            temp = cls.getLatestValue(db, cls._plantTemperatureCollectionName, serialID)
            light = cls.getLatestValue(db, cls._plantLightCollectionName, serialID)
            moisture = cls.getLatestValue(db, cls._plantMoistureCollectionName, serialID)
            soil = cls.getLatestValue(db, cls._plantSoilHumidityCollectionName, serialID)

            def getStatus(value, min_val, max_val, labels):
                if value is None:
                    return "Unknown"
                if value < min_val:
                    return labels[0]
                elif value > max_val:
                    return labels[2]
                else:
                    return labels[1]

            plant = {
                "serialID": serialID,
                "name": name,
                "temp": getStatus(temp, statRanges["Temperature"]["min"], statRanges["Temperature"]["max"], ["Cold", "OK", "Hot"]),
                "light": getStatus(light, statRanges["Light"]["min"], statRanges["Light"]["max"], ["Dark", "OK", "Bright"]),
                "humidity": getStatus(soil, statRanges["SoilHumidity"]["min"], statRanges["SoilHumidity"]["max"], ["Dry", "OK", "Soggy"]),
                "moisture": getStatus(moisture, statRanges["Moisture"]["min"], statRanges["Moisture"]["max"], ["Dry", "OK", "Saturated"]),
            }

            if any(plant[key] != "OK" for key in ["temp", "light", "humidity", "moisture"]):
                plantList.append(plant)
        return plantList

    @classmethod
    def GetDataSet(cls, serialIDList):
        db = cls._getFireStoreClient()
        
        dateStats = defaultdict(lambda: {"OK": 0, "not_OK": 0})
        
        sensor_types = {
            "Temperature": cls._plantTemperatureCollectionName,
            "Moisture": cls._plantMoistureCollectionName,
            "SoilHumidity": cls._plantSoilHumidityCollectionName,
            "Light": cls._plantLightCollectionName,
        }
        
        for serialID in serialIDList:
            plan_doc = db.collection(cls._plantPlanCollectionName).document(serialID).get()
            if not plan_doc.exists:
                continue
            stat_ranges = plan_doc.to_dict().get("Plan", {}).get("StatRanges", {})

            for stat_name, collection_name in sensor_types.items():
                range_min = stat_ranges.get(stat_name, {}).get("min")
                range_max = stat_ranges.get(stat_name, {}).get("max")
                if range_min is None or range_max is None:
                    continue
                
                logs_ref = db.collection(collection_name).document(serialID).collection("Logs")
                logs = logs_ref.stream()

                for log in logs:
                    data = log.to_dict()
                    timestamp = data.get("Time")
                    value = data.get("Value")
                    
                    if timestamp is None or value is None:
                        continue
                    
                    date_str = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")
                    
                    if range_min <= value <= range_max:
                        dateStats[date_str]["OK"] += 1
                    else:
                        dateStats[date_str]["not_OK"] += 1
        
        # Convert counts into percentages
        result = []
        for date, stats in sorted(dateStats.items()):
            total = stats["OK"] + stats["not_OK"]
            if total == 0:
                continue
            result.append({
                "date": date,
                "OK": round((stats["OK"] / total) * 100),
                "not_OK": round((stats["not_OK"] / total) * 100)
            })

        return result

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
    def checkStatRange(cls, statType, value, serialID):        
        db = cls._getFireStoreClient()
        
        plan_ref = db.collection(cls._plantPlanCollectionName).document(serialID).get()
        plan = plan_ref.to_dict()
        statRanges = plan['Plan']['StatRanges']
        range = statRanges[statType]
        
        if value > range['max']:
            content = statType + " is too high!"
            cls.Notify(serialID, content, 'warning')
        if value < range['min']:
            content = statType + " is too low!"
            cls.Notify(serialID, content, 'warning')
        
        
        
    @classmethod
    def addTemperatureEntry(cls, entry, serialID):        
        db = cls._getFireStoreClient()
        
        cls.checkStatRange('Temperature', entry['Value'], serialID)
        db.collection(cls._plantTemperatureCollectionName).document(serialID).collection('Logs').add(entry)
        

    @classmethod
    def addMoistureEntry(cls, entry, serialID):        
        db = cls._getFireStoreClient()
        
        cls.checkStatRange('Moisture', entry['Value'], serialID)
        db.collection(cls._plantMoistureCollectionName).document(serialID).collection('Logs').add(entry)

    @classmethod
    def addLightEntry(cls, entry, serialID):        
        db = cls._getFireStoreClient()
        
        cls.checkStatRange('Light', entry['Value'], serialID)
        db.collection(cls._plantLightCollectionName).document(serialID).collection('Logs').add(entry)

    @classmethod
    def addSoilHumidityEntry(cls, entry, serialID):        
        db = cls._getFireStoreClient()
        
        cls.checkStatRange('SoilHumidity', entry['Value'], serialID)
        db.collection(cls._plantSoilHumidityCollectionName).document(serialID).collection('Logs').add(entry)
        
    @classmethod
    def getPlan(cls, serialID):        
        db = cls._getFireStoreClient()
        
        planRef = db.collection(cls._plantPlanCollectionName).document(serialID).get()
        plan = planRef.to_dict()
        return plan['Plan']

    @staticmethod
    def getLatestValue(db, collection, serialID):
        statRef = db.collection(collection).document(serialID).get()

        log_query = (
            statRef.reference.collection("Logs")
            .order_by("Time", direction=firestore.Query.DESCENDING)
            .limit(1)
        )
        log_docs = log_query.stream()

        latest_log = next(log_docs, None)
        if latest_log and latest_log.exists:
            log_data = latest_log.to_dict()
            return log_data.get("Value")

        return None

    @classmethod
    def getPotStatus(cls, serialID):
        db = cls._getFireStoreClient()
        
        notificationRef = db.collection(cls._plantNotificationsCollectionName).document(serialID).get()
        notifications = notificationRef.to_dict()
        
        statusTemplate = {
            'Temperature': FireStoreClient.getLatestValue(db, cls._plantTemperatureCollectionName, serialID),
            'Light': FireStoreClient.getLatestValue(db, cls._plantLightCollectionName, serialID),
            'Moisture': FireStoreClient.getLatestValue(db, cls._plantMoistureCollectionName, serialID),
            'SoilHumidity': FireStoreClient.getLatestValue(db, cls._plantSoilHumidityCollectionName, serialID),
            'Notifications': notifications['Logs'],
            'Plan': cls.getPlan(serialID)
        }
        
        return statusTemplate

    # Document related
    _chatCollectionName = os.getenv("FIRESTORE_ASSISTANT_CHAT_COLLECTION")
    
    @classmethod
    def createChatDocument(cls):        
        db = cls._getFireStoreClient()
        
        resultTemplate = {
                            "Token": 0,
                            "History": []
                        }
        update_time, chatRef = db.collection(cls._chatCollectionName).add(resultTemplate)
        
        return chatRef.id, resultTemplate["History"]
    
    @classmethod
    def getChatHistory(cls, documentID):
        db = cls._getFireStoreClient()
        
        chatRef = db.collection(cls._chatCollectionName).document(documentID).get()
        chat = chatRef.to_dict()
        return chat['History']
    
    @classmethod
    def saveChatHistory(cls, chat, documentID):
        db = cls._getFireStoreClient()
        db.collection(cls._chatCollectionName).document(documentID).set(chat)