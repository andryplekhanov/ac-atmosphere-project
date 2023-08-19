from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from app_products.models import Category, Product, Image


class ImageInline(admin.TabularInline):
    model = Image


class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_short_title', 'category', 'total_price', 'available']
    list_filter = ['created', 'category', 'available']
    search_fields = ['title', ]
    save_on_top = True
    ordering = ['-created', ]
    inlines = [ImageInline, ]

    def get_short_title(self, obj):
        if len(obj.title) <= 50:
            return obj.title
        return f'{obj.title[:50]}...'
    get_short_title.short_description = 'заголовок'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
