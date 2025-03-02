from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Order
from ..selectors import OrderSelector
from ..serializers import OrderSerializer
from ..services import OrderService
from ..utils import CustomPaginator


class OrderViewSet(viewsets.ViewSet):
    http_method_names = ["get", "post", "put", "patch", "delete"]
    model = Order

    @extend_schema(
        summary="Retrieve a list of all orders",
        description="Retrieve a list of all orders with optional pagination",
        parameters=[
            OpenApiParameter(
                name="page",
                description="Page number for pagination. Type -1 to return all results without pagination.",
                required=False,
                type=int,
            ),
        ],
        responses={200: OrderSerializer(many=True)},
    )
    def list(self, request) -> Response:
        search_params = request.query_params.dict()
        page = search_params.get("page", 1)
        order_queryset = OrderSelector.list(search_params)

        if page == "-1":
            serializer = OrderSerializer(order_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        paginator = CustomPaginator()
        paginated_orders = paginator.paginate_queryset(order_queryset, request)
        serializer = OrderSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Retrieve a order",
        description="Retrieve a order by ID",
        responses={
            200: OrderSerializer,
            404: {"description": "Order not found"},
        },
    )
    def retrieve(self, request, pk=None) -> Response:
        instance = OrderSelector.retrieve(pk)
        serializer = OrderSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create a order",
        description="Create a new order",
        request=OrderSerializer,
        responses={
            201: OrderSerializer,
            400: {"description": "Invalid request payload"},
        },
    )
    def create(self, request) -> Response:
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_order = OrderService().create(serializer.validated_data)
        serializer = OrderSerializer(created_order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update a order",
        description="Update an existing order",
        request=OrderSerializer,
        responses={
            200: OrderSerializer,
            400: {"description": "Invalid request payload"},
            404: {"description": "Order not found"},
        },
    )
    def update(self, request, pk=None) -> Response:
        serializer = OrderSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = OrderSelector.retrieve(pk=pk)
        updated_order = OrderService(order_instance=instance).update(
            serializer.validated_data
        )
        serializer = OrderSerializer(updated_order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete a order",
        description="Soft-delete a order",
        responses={
            204: {"description": "Order deleted successfully"},
            404: {"description": "Order not found"},
        },
    )
    def destroy(self, request, pk=None) -> Response:
        instance = OrderSelector.retrieve(pk=pk)
        result = OrderService(order_instance=instance).destroy()
        return Response(data={"data": result}, status=status.HTTP_200_OK)
