from django.db import models
import uuid
from django.db.models import JSONField
from api.constants import LANGUAGES, CURRENCIES


class Company(models.Model):
    """
    This is a basic company model
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    language = models.CharField(max_length=10, choices=LANGUAGES)
    currency = models.CharField(max_length=10, choices=CURRENCIES)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ServiceArea(models.Model):
    """
    This is a basic company service area
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    geo_json = JSONField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccessToken(models.Model):
    """
    This is our Access token model for the API.
    """

    token = models.UUIDField(default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    expiry = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
