from django.shortcuts import get_object_or_404

from ..utils import BaseSelector
from ..models import Customer


class CustomerSelector(BaseSelector):
    @staticmethod
    def retrieve(pk: int) -> Customer:
        return get_object_or_404(Customer, pk=pk)

    @staticmethod
    def list(search_params: dict):
        return CustomerSelector.dynamic_filter(
            Customer.objects.filter(deleted=False), search_params
        )
