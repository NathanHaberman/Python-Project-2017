from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = []
        if len(postData['first_name']) < 2:
            errors.append('First name has to be at least 2 characters')
        elif len(postData['first_name']) > 255:
            errors.append('First name is too long')
        if len(postData['last_name']) < 2:
            errors.append('Last name has to be at least 2 characters')
        elif len(postData['last_name']) > 255:
            errors.append('Last name is too long')
        if len(postData['username']) < 8:
            errors.append('Username must be at least 8 characters')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Not a vaild email')
        if not postData['password'] == postData['confirm_password']:
            errors.append('Passwords do not match')
        elif len(postData['password']) < 8:
            errors.append('Password must be at least 8 characters')
        return errors
        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

class ProfileManager(models.Model):
    def validator(self, postData):
        errors = []
        if len(postData['sex']) > 6:
            errors.append("Please don't mess with the html")
        if postData['age'] < 18:
            errors.append('You must be at least 18 years of age to use this site')
        if postData['body_type'] < 1 or postData['body_type'] > 3:
            errors.append('Please select one of the three body types')
        if not postData['salary_range']:
            errors.append('Please select one of the salary ranges')
        return errors

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    desc = models.TextField()

    sex = models.CharField(max_length=6)

    age = models.PositiveIntegerField(default=18)

    height_feet = models.IntegerField(default=2)
    height_inch = models.IntegerField(default=0)

    body_type = models.IntegerField(default=2)

    salary_range = models.IntegerField(default=1)

    objects = ProfileManager()

class PreferenceManager(models.Model):
    def validator(self, postData):
        errors = []
        if postData['age_min'] < 18:
            errors.append('Age must be at least 18 years old')
        if postData['body_type'] < 1 or postData['body_type'] > 3:
            errors.append('Please select one of the three body types')
        if not postData['salary_range']:
            errors.append('Please select one of the salary ranges')
        return errors

class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preference')

    age_min = models.PositiveIntegerField(default=18)
    age_max = models.PositiveIntegerField(default=100)

    age_deal_breaker = models.BooleanField(default=False)


    height_feet_min = models.IntegerField(default=2)
    height_inch_min = models.IntegerField(default=0)

    height_feet_max = models.IntegerField(default=8)
    height_inch_max = models.IntegerField(default=0)

    height_deal_breaker = models.BooleanField(default=False)


    body_type = models.IntegerField(default=2)

    body_deal_breaker = models.BooleanField(default=False)


    salary_range = models.IntegerField(default=1)

    salary_deal_breaker = models.BooleanField(default=False)