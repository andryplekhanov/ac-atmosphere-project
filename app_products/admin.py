from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from app_products.models import Category, Product, Image, Parameter, ParameterName, ParameterValue


class ImageInline(admin.TabularInline):
    model = Image


class ParameterValueInline(admin.TabularInline):
    model = Parameter.products.through


class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_short_title', 'category', 'total_price', 'available']
    list_filter = ['created', 'category', 'available']
    search_fields = ['title', ]
    save_on_top = True
    ordering = ['-created', ]
    inlines = [ImageInline, ParameterValueInline]

    def get_short_title(self, obj):
        if len(obj.title) <= 50:
            return obj.title
        return f'{obj.title[:50]}...'
    get_short_title.short_description = 'заголовок'


class ParameterAdmin(admin.ModelAdmin):
    list_display = ['parameter', 'value', ]
    list_filter = ['parameter']
    save_on_top = True


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(ParameterName)
admin.site.register(ParameterValue)
