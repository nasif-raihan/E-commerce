from dataclasses import dataclass

from django.contrib.auth.models import User

from ..utils import BaseService
from ..models import Customer


@dataclass
class CustomerService(BaseService):
    customer_instance: Customer = None
    user_instance: User = None

    def create(self, data: dict) -> Customer:
        return Customer.objects.create(**data)

    def update(self, data: dict) -> Customer:
        for key, value in data.items():
            setattr(self.customer_instance, key, value)
        self.customer_instance.save()
        return self.customer_instance

    def destroy(self) -> dict:
        if not self.customer_instance:
            raise RuntimeError("No customer instance provided")

        if self.user_instance:
            self.customer_instance.user_deleted = self.user_instance

        self.customer_instance.enabled = False
        self.customer_instance.deleted = True
        self.customer_instance.save()

        return {
            "enabled": self.customer_instance.enabled,
            "deleted": self.customer_instance.deleted,
        }
