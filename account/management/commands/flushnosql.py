from django.core.management.base import BaseCommand
from plant.modules.firestoreTools import FireStoreClient

class Command(BaseCommand):
    help = 'Clear everything in nosql database'
    
    def handle(self, *args, **options):
        FireStoreClient.nuke()
        return