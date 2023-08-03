from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSW(models.Model):
    PW_TYPES = [('confidential', 'c'),('sharable', 's')]
    title = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=PW_TYPES, max_length=12)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    
    def __str__(self):
        return self.title