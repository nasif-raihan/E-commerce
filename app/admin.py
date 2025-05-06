from django.contrib import admin

from .models import Cart, Customer, Product, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "city", "locality", "zipcode", "division")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "brand",
        "selling_price",
        "discounted_price",
        "product_image",
        "created",
        "modified",
    )
    list_filter = ("category", "brand", "created")  # Filters in the sidebar
    search_fields = ("title", "brand", "description")  # Search box
    ordering = ("-created",)  # Default ordering
    readonly_fields = ("created", "modified")  # Non-editable fields
    fieldsets = (
        (None, {
            "fields": ("title", "category", "brand", "description")
        }),
        ("Pricing & Image", {
            "fields": ("selling_price", "discounted_price", "product_image")
        }),
        ("Timestamps", {
            "fields": ("created", "modified")
        }),
    )



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "quantity",
        "ordered_date",
        "status",
        "user",
        "customer",
        "product",
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "quantity", "product")
