import random
import string
from django.db import models
from account.models import Account

def GeneratePotKey():
    charset = string.ascii_uppercase + string.digits
    return "-".join("".join(random.choice(charset) for _ in range(4)) for _ in range(3))

class PotRegistry(models.Model):
    # Normal fields
    Name        = models.CharField(max_length=50, blank=False, null=False, default="Smart Plant Pot")
    SerialID    = models.CharField(max_length=20, blank=False, null=False, unique=True, editable=False)
    Key         = models.CharField(max_length=14, blank=False, null=False, editable=False, default="XXXX-XXXX-XXXX")
    
    # Foreign keys
    Account     = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    
    # Admin page display function
    def __str__(self):
        return f"{self.id} | {self.Name} | {self.SerialID}"



# TODO: Generate a JSON on creation
class Plan(models.Model):
    # Normal fields
    Name        = models.CharField(max_length=50,  blank=False, null=False, default="My plant plan")
    JSON        = models.CharField(max_length=255, blank=False, null=False, default="Some JSON")   
    
    # Foreign keys
    Account     = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    
    # Admin page display function
    def __str__(self):
        return f"{self.id} | {self.Name}"