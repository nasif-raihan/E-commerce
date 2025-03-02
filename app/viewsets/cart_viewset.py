from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Cart
from ..selectors import CartSelector
from ..serializers import CartSerializer
from ..services import CartService
from ..utils import CustomPaginator


class CartViewSet(viewsets.ViewSet):
    http_method_names = ["get", "post", "put", "patch", "delete"]
    model = Cart

    @extend_schema(
        summary="Retrieve a list of all carts",
        description="Retrieve a list of all carts with optional pagination",
        parameters=[
            OpenApiParameter(
                name="page",
                description="Page number for pagination. Type -1 to return all results without pagination.",
                required=False,
                type=int,
            ),
        ],
        responses={200: CartSerializer(many=True)},
    )
    def list(self, request) -> Response:
        search_params = request.query_params.dict()
        page = search_params.get("page", 1)
        cart_queryset = CartSelector.list(search_params)

        if page == "-1":
            serializer = CartSerializer(cart_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        paginator = CustomPaginator()
        paginated_orders = paginator.paginate_queryset(cart_queryset, request)
        serializer = CartSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Retrieve a cart",
        description="Retrieve a cart by ID",
        responses={
            200: CartSerializer,
            404: {"description": "Cart not found"},
        },
    )
    def retrieve(self, request, pk=None) -> Response:
        instance = CartSelector.retrieve(pk)
        serializer = CartSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create a cart",
        description="Create a new cart",
        request=CartSerializer,
        responses={
            201: CartSerializer,
            400: {"description": "Invalid request payload"},
        },
    )
    def create(self, request) -> Response:
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_cart = CartService().create(serializer.validated_data)
        serializer = CartSerializer(created_cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update a cart",
        description="Update an existing cart",
        request=CartSerializer,
        responses={
            200: CartSerializer,
            400: {"description": "Invalid request payload"},
            404: {"description": "Cart not found"},
        },
    )
    def update(self, request, pk=None) -> Response:
        serializer = CartSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = CartSelector.retrieve(pk=pk)
        updated_cart = CartService(cart_instance=instance).update(
            serializer.validated_data
        )
        serializer = CartSerializer(updated_cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete a cart",
        description="Soft-delete a cart",
        responses={
            204: {"description": "Cart deleted successfully"},
            404: {"description": "Cart not found"},
        },
    )
    def destroy(self, request, pk=None) -> Response:
        instance = CartSelector.retrieve(pk=pk)
        result = CartService(cart_instance=instance).destroy()
        return Response(data={"data": result}, status=status.HTTP_200_OK)
