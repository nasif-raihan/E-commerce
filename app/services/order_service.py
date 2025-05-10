from dataclasses import dataclass

from django.contrib.auth.models import User

from ..utils import BaseService
from ..models import Order


@dataclass
class OrderService(BaseService):
    order_instance: Order = None
    user_instance: User = None

    def create(self, data: dict) -> Order:
        return Order.objects.create(**data)

    def update(self, data: dict) -> Order:
        for key, value in data.items():
            setattr(self.order_instance, key, value)
        self.order_instance.save()
        return self.order_instance

    def destroy(self) -> dict:
        if not self.order_instance:
            raise RuntimeError("No order instance provided")

        if self.user_instance:
            self.order_instance.user_deleted = self.user_instance

        self.order_instance.enabled = False
        self.order_instance.deleted = True
        self.order_instance.save()

        return {
            "enabled": self.order_instance.enabled,
            "deleted": self.order_instance.deleted,
        }
