from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import CartViewSet, CustomerViewSet, OrderViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"carts", CartViewSet, basename="cart")
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [path("", include(router.urls))]
