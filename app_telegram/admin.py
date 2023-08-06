from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from app_telegram.models import TGUser, CallRequest


class TGUserAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'username', 'phone_number', 'fullname', 'created']
    list_filter = ['created',]
    search_fields = ['username', 'fullname', 'tg_id', 'phone_number']
    save_on_top = True


class CallRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'get_user_fullname', 'get_user_phone', 'created']
    list_filter = ['created', 'status']
    search_fields = ['from_user__tg_id', 'from_user__username', 'from_user__phone_number']
    save_on_top = True

    def get_user_phone(self, obj):
        if obj.from_user:
            return f'{obj.from_user.phone_number}'
        return _('пользователь удалён')
    get_user_phone.short_description = _('Телефон')

    def get_user_fullname(self, obj):
        if obj.from_user:
            return f'{obj.from_user.fullname}'
        return _('пользователь удалён')
    get_user_fullname.short_description = _('Имя')


admin.site.register(TGUser, TGUserAdmin)
admin.site.register(CallRequest, CallRequestAdmin)
