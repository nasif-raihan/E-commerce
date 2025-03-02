from django.contrib.auth.models import User
from django.db import models

from ..utils import BaseModel


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(to="app.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Cart Item: {self.product.title} (x{self.quantity})"
