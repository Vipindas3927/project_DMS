from django.db import models


# Create your models here.


class batch(models.Model):
    class_name = models.CharField(max_length=255)
    date_of_join = models.DateField(null=True)
    semester = models.CharField(max_length=255)
    scheme = models.BigIntegerField(null=False)


class scheme(models.Model):
    scheme = models.CharField(max_length=255, null=False)
    

class subject(models.Model):
    code = models.CharField(max_length=255, null=False)
    subject_name = models.CharField(max_length=255, null=False)
    credit = models.BigIntegerField(null=False)
    scheme = models.BigIntegerField(null=False)


class Internal_mark(models.Model):
    university_no = models.CharField(max_length=255, null=False)
    subject_code = models.CharField(max_length=255, null=False)
    
    exm_type = [
        ('Assignment 1','Assignment 1'),
        ('Assignment 2','Assignment 2'),
        ('Internal 1','Internal 1'),
        ('Internal 2','Internal 2'),
        ('Others','Others')
    ]
    exam_type = models.CharField(max_length=255, null=False, choices=exm_type)
    mark = models.FloatField(null=False)
    

class semester_result(models.Model):
    university_no = models.CharField(max_length=255, null=False)
    subject_code = models.CharField(max_length=255, null=False)
    grade_point = models.BigIntegerField(null=False)
    no_of_chanses = models.BigIntegerField(null=False)
    semester = models.CharField(max_length=255, null=False)
    scheme = models.CharField(max_length=255, null=False)






    


