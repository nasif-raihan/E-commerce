from django.shortcuts import get_object_or_404

from ..utils import BaseSelector
from ..models import Product


class ProductSelector(BaseSelector):
    @staticmethod
    def retrieve(pk: int) -> Product:
        return get_object_or_404(Product, pk=pk)

    @staticmethod
    def list(search_params: dict):
        return ProductSelector.dynamic_filter(
            Product.objects.filter(deleted=False), search_params
        )
