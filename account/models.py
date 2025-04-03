from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Manager class for user account with customized create user function
class AccountManager(BaseUserManager):
    # Function to create new user
    # By default django will not allow no password
    def create_user(self, email, Name, password=None):
        # Raise error if there is no email
        if not email:
            raise ValueError('User must have an email address')
        
        # Normalizer normalizing email (lowercasing,...) 
        email = self.normalize_email(email)
        user = self.model(email=email, Name=Name)
        
        # Hashing password for security reasons
        user.set_password(password)
        
        # Finally save the user
        user.save()
        return user

# Custom user model goes here.
class Account(AbstractBaseUser, PermissionsMixin):
    # Important user fields
    email           = models.EmailField(max_length=255, unique=True)
    Name            = models.CharField(max_length=50)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_manufacturer = models.BooleanField(default=False)
    
    # Other informative user fields
    PhoneNumber     = models.CharField(max_length=20, null=True, blank=True)
    DateOfBirth     = models.DateTimeField(null=True)
    Gender          = models.CharField(max_length=20, null=True, blank=True)
    Address         = models.CharField(max_length=50, null=True, blank=True)
    
    ImageBase64     = models.TextField(null=True, blank=True)  
    
    # Choosing email as username for login/signup
    USERNAME_FIELD = 'email'
    
    # Required fields, must not be null
    REQUIRED_FIELDS = ['Name']
    
    objects = AccountManager()
    
    # Admin page default function
    def __str__(self):
        return self.Name 