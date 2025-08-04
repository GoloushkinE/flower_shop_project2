from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available']
    
    # === НАЧАЛО ИСПРАВЛЕНИЯ ===
    
    list_filter = ['available', 'created', 'updated', 'category']
    
    # === КОНЕЦ ИСПРАВЛЕНИЯ ===

    list_editable = ['price', 'stock', 'available']
    
    fields = (
        'name',
        'slug',
        'category',
        'image',
        'description',
        'price',
        'stock',
        'available'
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}