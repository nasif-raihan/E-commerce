from django.contrib.auth.models import User
from django.db import models

from ..utils import BaseModel

DIVISIONS = {
    "dhaka": "Dhaka",
    "khulna": "Khulna",
    "sylhet": "Sylhet",
    "rangpur": "Rangpur",
    "barishal": "Barishal",
    "rajshahi": "Rajshahi",
    "mymensingh": "Mymensingh",
    "chattogram": "Chattogram",
}


class Customer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    division = models.CharField(choices=DIVISIONS, max_length=100)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.id}"
