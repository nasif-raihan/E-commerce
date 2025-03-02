from django.contrib.auth.models import User
from django.db import models

from ..utils import BaseModel

STATUS = {
    "packed": "Packed",
    "accepted": "Accepted",
    "canceled": "Canceled",
    "delivered": "Delivered",
    "on_the_way": "On the way",
}


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(to="app.Customer", on_delete=models.CASCADE)
    product = models.ForeignKey(to="app.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=100)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"Order {self.id} - {self.status}"
