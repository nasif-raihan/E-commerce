from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Customer
from ..selectors import CustomerSelector
from ..serializers import CustomerSerializer
from ..services import CustomerService
from ..utils import CustomPaginator


class CustomerViewSet(viewsets.ViewSet):
    http_method_names = ["get", "post", "put", "patch", "delete"]
    model = Customer

    @extend_schema(
        summary="Retrieve a list of all customers",
        description="Retrieve a list of all customers with optional pagination",
        parameters=[
            OpenApiParameter(
                name="page",
                description="Page number for pagination. Type -1 to return all results without pagination.",
                required=False,
                type=int,
            ),
        ],
        responses={200: CustomerSerializer(many=True)},
    )
    def list(self, request) -> Response:
        search_params = request.query_params.dict()
        page = search_params.get("page", 1)
        customer_queryset = CustomerSelector.list(search_params)

        if page == "-1":
            serializer = CustomerSerializer(customer_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        paginator = CustomPaginator()
        paginated_orders = paginator.paginate_queryset(customer_queryset, request)
        serializer = CustomerSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Retrieve a customer",
        description="Retrieve a customer by ID",
        responses={
            200: CustomerSerializer,
            404: {"description": "Customer not found"},
        },
    )
    def retrieve(self, request, pk=None) -> Response:
        instance = CustomerSelector.retrieve(pk)
        serializer = CustomerSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create a customer",
        description="Create a new customer",
        request=CustomerSerializer,
        responses={
            201: CustomerSerializer,
            400: {"description": "Invalid request payload"},
        },
    )
    def create(self, request) -> Response:
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_customer = CustomerService().create(serializer.validated_data)
        serializer = CustomerSerializer(created_customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update a customer",
        description="Update an existing customer",
        request=CustomerSerializer,
        responses={
            200: CustomerSerializer,
            400: {"description": "Invalid request payload"},
            404: {"description": "Customer not found"},
        },
    )
    def update(self, request, pk=None) -> Response:
        serializer = CustomerSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = CustomerSelector.retrieve(pk=pk)
        updated_customer = CustomerService(customer_instance=instance).update(
            serializer.validated_data
        )
        serializer = CustomerSerializer(updated_customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete a customer",
        description="Soft-delete a customer",
        responses={
            204: {"description": "Customer deleted successfully"},
            404: {"description": "Customer not found"},
        },
    )
    def destroy(self, request, pk=None) -> Response:
        instance = CustomerSelector.retrieve(pk=pk)
        result = CustomerService(customer_instance=instance).destroy()
        return Response(data={"data": result}, status=status.HTTP_200_OK)
