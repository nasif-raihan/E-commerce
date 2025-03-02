from django.conf import settings
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPaginator(PageNumberPagination):
    def __init__(self, page_size=settings.PAGE_SIZE):
        self.page_size = page_size

    def get_paginated_response(self, data):
        return Response(
            {
                "paginator": {
                    "total_items": self.page.paginator.count,
                    "num_pages": self.page.paginator.num_pages,
                    "page_size": self.page_size,
                    "current_page": self.page.number,
                    "next_page": (
                        self.page.next_page_number() if self.page.has_next() else None
                    ),
                    "prev_page": (
                        self.page.previous_page_number()
                        if self.page.has_previous()
                        else None
                    ),
                    "has_next_page": self.page.has_next(),
                    "has_prev_page": self.page.has_previous(),
                },
                "results": data,
            },
            status=status.HTTP_200_OK,
        )
