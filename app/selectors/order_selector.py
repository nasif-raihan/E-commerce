from django.shortcuts import get_object_or_404

from ..utils import BaseSelector
from ..models import Order


class OrderSelector(BaseSelector):
    @staticmethod
    def retrieve(pk: int) -> Order:
        return get_object_or_404(Order, pk=pk)

    @staticmethod
    def list(search_params: dict):
        return OrderSelector.dynamic_filter(
            Order.objects.filter(deleted=False), search_params
        )
