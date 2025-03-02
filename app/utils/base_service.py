from abc import ABC, abstractmethod

from django.db.models import Model


class BaseService(ABC):
    @abstractmethod
    def create(self, data: dict) -> Model:
        raise NotImplementedError("Implement create method")

    @abstractmethod
    def update(self, data: dict) -> Model:
        raise NotImplementedError("Implement update method")

    @abstractmethod
    def destroy(self) -> dict:
        raise NotImplementedError("Implement destroy method")
