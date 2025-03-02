from dataclasses import dataclass
from typing import Dict

from django.contrib.auth.models import User

from .base_service import BaseService
from ..models import Product


@dataclass
class ProductService(BaseService):
    product_instance: Product = None
    user_instance: User = None

    def create(self, data: dict) -> Product:
        return Product.objects.create(**data)

    def update(self, data: dict) -> Product:
        for key, value in data.items():
            setattr(self.product_instance, key, value)
        self.product_instance.save()
        return self.product_instance

    def destroy(self) -> Dict[str, bool]:
        if not self.product_instance:
            raise RuntimeError("No product instance provided")

        if self.user_instance:
            self.product_instance.user_deleted = self.user_instance

        self.product_instance.enabled = False
        self.product_instance.deleted = True
        self.product_instance.save()

        return {
            "enabled": self.product_instance.enabled,
            "deleted": self.product_instance.deleted,
        }
