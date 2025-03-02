from django.core.management.base import BaseCommand
from plant.modules.firestoreTools import FireStoreClient

class Command(BaseCommand):
    help = 'Initiate the NoSQL database'
    
    def handle(self, *args, **options):
        FireStoreClient.initFirestoreDatabase()
        return