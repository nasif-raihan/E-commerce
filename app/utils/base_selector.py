from django.core.exceptions import FieldError
from django.db.models import Q, QuerySet
from django.http import QueryDict


class BaseSelector:
    fields_map: dict[str, str] = {}

    @classmethod
    def dynamic_filter(
        cls,
        queryset: QuerySet,
        search_params: QueryDict | dict,
        order_by: list = None,
        limit: int = None,
    ) -> QuerySet:
        query_conditions = []
        if isinstance(search_params, QueryDict):
            items = search_params.lists()
        else:
            items = search_params.items()

        limit_value = search_params.get("limit")
        if limit_value is not None:
            try:
                limit = int(limit_value)
            except (ValueError, TypeError):
                pass

        for key, values in items:
            if key == "limit":
                continue

            query_key = cls.fields_map.get(key)
            if not query_key:
                continue

            values = values if isinstance(values, list) else [values]
            query_conditions.append(
                Q(**{query_key: values if query_key.endswith("__in") else values[0]})
            )

        try:
            filtered_queryset = queryset.filter(*query_conditions)
            if order_by:
                filtered_queryset = filtered_queryset.order_by(*order_by)
            return filtered_queryset[:limit] if limit else filtered_queryset

        except FieldError as e:
            raise FieldError(f"Invalid field in filtering: {e}") from e
