from dataclasses import dataclass
from typing import Dict

from django.contrib.auth.models import User

from .base_service import BaseService
from ..models import Cart


@dataclass
class CartService(BaseService):
    cart_instance: Cart = None
    user_instance: User = None

    def create(self, data: dict) -> Cart:
        return Cart.objects.create(**data)

    def update(self, data: dict) -> Cart:
        for key, value in data.items():
            setattr(self.cart_instance, key, value)
        self.cart_instance.save()
        return self.cart_instance

    def destroy(self) -> Dict[str, bool]:
        if not self.cart_instance:
            raise RuntimeError("No cart instance provided")

        if self.user_instance:
            self.cart_instance.user_deleted = self.user_instance

        self.cart_instance.enabled = False
        self.cart_instance.deleted = True
        self.cart_instance.save()

        return {
            "enabled": self.cart_instance.enabled,
            "deleted": self.cart_instance.deleted,
        }
