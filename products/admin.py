from django.contrib import admin
from .models import (
    Category,
    Product,
    File,
    Cart,
    CartItem,
    Comment,
    Contact,
    Customer,
    Order,
    OrderItem,
)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["customer", "created_at", "is_active"]
    list_filter = ["created_at", "is_active"]
    search_fields = ["customer"]
    inlines = [CartItemInline]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "phone"]
    list_filter = ["date"]
    search_fields = ["customer"]
    inlines = [OrderItemInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "customer", "stars", "is_approved", "created_at")
    list_filter = ("is_approved", "stars", "created_at")
    search_fields = ("text", "customer__user__username", "product__title")
    ordering = ("-created_at",)


admin.site.register(Contact)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "parent", "is_enable", "created_at")
    list_filter = ("is_enable", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"title": ("title",)}
    ordering = ("-created_at",)


class FileInlineModelAdmin(admin.StackedInline):
    model = File
    extra = 0
    fields = ["title", "file", "is_enable"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "is_enable",
        "created_at",
        "is_off",
        "is_new",
        "is_stock",
    )
    list_filter = ("created_at", "is_off", "is_new", "is_stock")
    search_fields = ("title", "description", "is_off", "is_new", "is_stock")
    filter_horizontal = ("categories",)
    ordering = ("-created_at",)
    inlines = [FileInlineModelAdmin]
