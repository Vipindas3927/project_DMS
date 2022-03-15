from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_hod = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        category = ''
        if self.is_staff :
            category = 'Staff'
        elif self.is_hod:
            category = 'HOD'
        elif self.is_student:
            category = 'Student'
        name = self.first_name +" "+ self.last_name + " - " + category
        return name

'''class User(AbstractBaseUser):
    is_hod = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
'''    
    



