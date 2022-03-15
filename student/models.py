from django.db import models


# Create your models here.
class profile_student(models.Model):
    register_no = models.CharField(max_length=255)
    university_no = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    branch = models.CharField(max_length=255, null=True)
    aadhar_no = models.BigIntegerField(unique=True, null=True)
    address = models.CharField(max_length=255, null=True)
    phone_no = models.BigIntegerField(unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    sex = models.CharField(max_length=10, null=True, choices=[('Female', 'Female'), ('Male', 'Male'), ('Others', 'Others')])
    date_of_birth = models.DateField(unique=False, null=True)
    nationality = models.CharField(max_length=255, null=True)
    religion = models.CharField(max_length=255, null=True)
    caste = models.CharField(max_length=255, null=True)
    native_place = models.CharField(max_length=255, null=True)
    batch = models.BigIntegerField(unique=False, null=False)
    scheme_id = models.BigIntegerField(unique=False, null=False)


    blood_groups = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=10, choices=blood_groups, null=True)
    hobbies = models.CharField(max_length=100, null=True)
    photo = models.ImageField(upload_to='images/', null=True, default='images/user_default_image.png')
    sign = models.ImageField(upload_to='images/', null=True)

    
    
    def __str__(self):
        name = self.first_name +" "+ self.last_name
        return name