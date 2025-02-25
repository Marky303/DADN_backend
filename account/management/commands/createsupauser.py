from django.core.management.base import BaseCommand
from account.models import Account

class Command(BaseCommand):
    help = 'Create super user (nhien/1234) to edit in admin site'
    
    # Create new usersuper (nhien/1234)
    def handle(self, *args, **options):
        user = Account.objects.create_user(Name='nhien',email='nhien')
        user.set_password("1234")
        
        # Set super user tags
        user.is_superuser       = True
        user.is_active          = True
        user.is_staff           = True
        user.is_manufacturer    = True
        
        # Save new superuser and notify
        user.save()
        print("Created supa user")
        
        return