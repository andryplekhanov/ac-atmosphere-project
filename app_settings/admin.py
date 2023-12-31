from django.contrib import admin
from django.contrib.auth.models import Group

from app_settings.models import AdminItem, AdminsSettings, CompanySettings, CurrencySettings
from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
    PeriodicTask,
)


class CompanySettingsAdmin(admin.ModelAdmin):
    """ В админ-панели нужно создать экземпляр с настройками """

    def has_add_permission(self, request, obj=None):
        """ Запрещает создать более 1го экземпляра с настройками """
        if not self.model.objects.all():
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        """ Запрещает удалять экземпляр с настройками """
        return False


class CurrencySettingsAdmin(admin.ModelAdmin):
    """ В админ-панели нужно создать экземпляр с настройками """

    list_display = ['dollar_exchange_rate', 'updated']
    readonly_fields = ["current_rate", 'updated']
    save_on_top = True

    def has_add_permission(self, request, obj=None):
        """ Запрещает создать более 1го экземпляра с настройками """
        if not self.model.objects.all():
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        """ Запрещает удалять экземпляр с настройками """
        return False


class AdminItemInline(admin.TabularInline):
    model = AdminItem


class AdminsSettingsAdmin(admin.ModelAdmin):
    """ В админ-панели нужно создать экземпляр с настройками """

    inlines = [AdminItemInline]

    def has_add_permission(self, request, obj=None):
        """ Запрещает создать более 1го экземпляра с настройками """
        if not self.model.objects.all():
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        """ Запрещает удалять экземпляр с настройками """
        return False


admin.site.unregister(Group)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.register(CompanySettings, CompanySettingsAdmin)
admin.site.register(AdminsSettings, AdminsSettingsAdmin)
admin.site.register(CurrencySettings, CurrencySettingsAdmin)
