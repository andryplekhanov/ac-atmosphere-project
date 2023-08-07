from django.contrib import admin

from app_telegram.models import TGUser, CallRequest, TGMessage


class TGUserAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'phone_number', 'fullname', 'created']
    list_filter = ['created',]
    search_fields = ['fullname', 'tg_id', 'phone_number']
    save_on_top = True


class CallRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'get_user_fullname', 'get_user_phone', 'created']
    list_filter = ['created', 'status']
    search_fields = ['from_user__tg_id', 'from_user__phone_number', 'from_user__fullname']
    save_on_top = True

    def get_user_phone(self, obj):
        if obj.from_user:
            return f'{obj.from_user.phone_number}'
        return 'пользователь удалён'
    get_user_phone.short_description = 'Телефон'

    def get_user_fullname(self, obj):
        if obj.from_user:
            return f'{obj.from_user.fullname}'
        return 'пользователь удалён'
    get_user_fullname.short_description = 'Имя'


class TGMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'get_user_fullname', 'get_user_phone', 'created']
    list_filter = ['created', 'status']
    search_fields = ['from_user__tg_id', 'from_user__fullname', 'from_user__phone_number']
    save_on_top = True

    def get_user_phone(self, obj):
        if obj.from_user:
            return f'{obj.from_user.phone_number}'
        return 'пользователь удалён'
    get_user_phone.short_description = 'Телефон'

    def get_user_fullname(self, obj):
        if obj.from_user:
            return f'{obj.from_user.fullname}'
        return 'пользователь удалён'
    get_user_fullname.short_description = 'Имя'


admin.site.register(TGUser, TGUserAdmin)
admin.site.register(CallRequest, CallRequestAdmin)
admin.site.register(TGMessage, TGMessageAdmin)
