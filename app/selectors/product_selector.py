from django.shortcuts import get_object_or_404

from ..models import Product
from ..utils import BaseSelector


class ProductSelector(BaseSelector):
    fields_map = {
        "category": "category",
        "brand": "brand__icontains",
        "title": "title__icontains",
        "selling_price_low": "selling_price__gte",
        "selling_price_high": "selling_price__lte",
        "discounted_price_low": "discounted_price__gte",
        "discounted_price_high": "discounted_price__lte",
    }

    @staticmethod
    def retrieve(pk: int) -> Product:
        return get_object_or_404(Product, pk=pk)

    @staticmethod
    def list(search_params: dict):
        return ProductSelector.dynamic_filter(
            Product.objects.filter(deleted=False), search_params
        )
