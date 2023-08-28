from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class UserSW(models.Model):
    PW_TYPES = [('confidential', 'confidential'),('sharable', 'sharable')]
    title = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=PW_TYPES, max_length=12)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=False, blank=False)
    
    def __str__(self):
        return self.title