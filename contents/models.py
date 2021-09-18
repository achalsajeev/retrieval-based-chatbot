from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
from pathlib import Path

class User(AbstractUser):
  is_admin = models.BooleanField(default=False)
  is_customer = models.BooleanField(default=False)
  is_human_agent = models.BooleanField(default=False)
  is_company = models.BooleanField(default=False)
  is_bot_agent = models.BooleanField(default=False)

class Admin(models.Model):
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.admin.username
        
class Customer(models.Model):
    customer = models.OneToOneField(
      settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    mobile_no = models.BigIntegerField(default=0)
    description = models.TextField()

    def __str__(self):
        return self.customer.username

class Company(models.Model):
    company = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mobile_no = models.BigIntegerField(default=0)
    def __str__(self):
        return self.company.username

class Human_agent(models.Model):
    human_agent = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mobile_no = models.BigIntegerField(default=0)
    def __str__(self):
        return self.human_agent.username

class Bot_agent(models.Model):
    bot_agent = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.bot_agent.username

class Domains(models.Model):
    id = models.AutoField(primary_key=True)
    domain = models.CharField(max_length=100, default=None)
    client = models.CharField(max_length=100, default=None)

class Intents(models.Model):
    id = models.AutoField(primary_key=True)
    intent = models.CharField(max_length=500, default=None)
    user_say = models.CharField(max_length=5000, default=None)
    response = models.CharField(max_length=5000, default=None)
    domain = models.ForeignKey(Domains, related_name='domain_name', blank=True, on_delete=models.CASCADE)

class Entity(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.CharField(max_length=1000, default=None)
    entity_type = models.CharField(max_length=1000, default=None)
    value = models.CharField(max_length=1000, default=None)
    synonyms = models.CharField(max_length=1000, default=None)
    intents = models.ForeignKey(Intents, related_name='intents', blank=True, on_delete=models.CASCADE)

class Conversations(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.CharField(max_length=50, default=None)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    feedback = models.CharField(max_length=50,blank=True)
    remarks = models.CharField(max_length=100, blank=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversations, related_name='conversation', on_delete=models.CASCADE, blank=True)
    msg = models.CharField(max_length=5000, blank=True)
    response = models.TextField(blank=True)

def filepath(instance, filename):
    path = "files/"
    formatted = str(uuid.uuid4()) + filename
    return Path(path, formatted)

class TrainFiles(models.Model):
    id = models.AutoField(primary_key=True)
    trainfile = models.FileField(upload_to=filepath)
    client = models.CharField(max_length=100, blank=True)
    domain = models.CharField(max_length=100)
    upload_date = models.DateField(blank=True)