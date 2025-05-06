from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Product
from ..selectors import ProductSelector
from ..serializers import ProductSerializer
from ..services import ProductService
from ..utils import CustomPaginator


class ProductViewSet(viewsets.ViewSet):
    http_method_names = ["get", "post", "put", "patch", "delete"]
    model = Product

    @extend_schema(
        summary="Retrieve a list of all products",
        description="Retrieve a list of all products with optional pagination",
        parameters=[
            OpenApiParameter(
                name="page",
                description="Page number for pagination. Type -1 to return all results without pagination.",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="category",
                description="Filter products by category.",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="brand",
                description="Filter products by brand.",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="selling_price_low",
                description="Filter products by minimum selling price.",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="selling_price_high",
                description="Filter products by maximum selling price.",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="discounted_price_low",
                description="Filter products by minimum discounted price.",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="discounted_price_high",
                description="Filter products by maximum discounted price.",
                required=False,
                type=int,
            ),
        ],
        responses={200: ProductSerializer(many=True)},
    )
    def list(self, request) -> Response:
        search_params = request.query_params.dict()
        page = search_params.get("page", 1)
        product_queryset = ProductSelector.list(search_params)

        if page == "-1":
            serializer = ProductSerializer(product_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        paginator = CustomPaginator()
        paginated_orders = paginator.paginate_queryset(product_queryset, request)
        serializer = ProductSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Retrieve a product",
        description="Retrieve a product by ID",
        responses={
            200: ProductSerializer,
            404: {"description": "Product not found"},
        },
    )
    def retrieve(self, request, pk=None) -> Response:
        instance = ProductSelector.retrieve(pk)
        serializer = ProductSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create a product",
        description="Create a new product",
        request=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: {"description": "Invalid request payload"},
        },
    )
    def create(self, request) -> Response:
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_product = ProductService().create(serializer.validated_data)
        serializer = ProductSerializer(created_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update a product",
        description="Update an existing product",
        request=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: {"description": "Invalid request payload"},
            404: {"description": "Product not found"},
        },
    )
    def update(self, request, pk=None) -> Response:
        serializer = ProductSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = ProductSelector.retrieve(pk=pk)
        updated_product = ProductService(product_instance=instance).update(
            serializer.validated_data
        )
        serializer = ProductSerializer(updated_product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete a product",
        description="Soft-delete a product",
        responses={
            204: {"description": "Product deleted successfully"},
            404: {"description": "Product not found"},
        },
    )
    def destroy(self, request, pk=None) -> Response:
        instance = ProductSelector.retrieve(pk=pk)
        result = ProductService(product_instance=instance).destroy()
        return Response(data={"data": result}, status=status.HTTP_200_OK)
