from django.contrib import admin
from .models import Category, Product, File


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
    fields = ['title','file','is_enable']



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_enable", "created_at",'is_off','is_new','is_stock')
    list_filter = ("created_at","is_off","is_new","is_stock")
    search_fields = ("title", "description","is_off","is_new","is_stock")
    filter_horizontal = ("categories",)  
    ordering = ("-created_at",)
    inlines = [FileInlineModelAdmin]




