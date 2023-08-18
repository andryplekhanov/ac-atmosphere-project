from django.contrib import admin

from app_orders.models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'user', 'delivery_type', 'get_total_cost', 'discount', 'paid', 'created', 'updated']
    list_filter = ['status', 'paid', 'created', 'updated']
    search_fields = ['id', 'user__tg_id', 'user__username', 'user__fullname', 'user__phone_number', 'address', 'comment']
    save_on_top = True
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
