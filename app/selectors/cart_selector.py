from django.shortcuts import get_object_or_404

from .base_selector import BaseSelector
from ..models import Cart


class CartSelector(BaseSelector):
    @staticmethod
    def retrieve(pk: int) -> Cart:
        return get_object_or_404(Cart, pk=pk)

    @staticmethod
    def list(search_params: dict):
        return CartSelector.dynamic_filter(
            Cart.objects.filter(deleted=False), search_params
        )
