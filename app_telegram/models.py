from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True
        ordering = ('-created',)

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('дата обновления'))


class TGUser(TimeBasedModel):
    # Раскомментировать, если нужна связка с аккаунтами с сайта
    # user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('пользователь'))
    tg_id = models.BigIntegerField(unique=True, db_index=True, verbose_name=_('id Telegram'))
    fullname = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('имя'))
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('телефон'), db_index=True)
    is_banned = models.BooleanField(default=False, verbose_name='забанен')

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def __str__(self):
        return f'user id {self.tg_id}'


class CallRequest(TimeBasedModel):
    STATUS_CHOICES = (
        ("0", _("Закрытая")),
        ("1", _("Новая")),
        ("2", _("В процессе")),
        ("3", _("Не дозвонился")),
        ("4", _("Перезвонить")),
        ("5", "Спам (заблокировать)"),
    )
    from_user = models.ForeignKey('TGUser', on_delete=models.SET_NULL, null=True, related_name='calls',
                                  verbose_name=_('пользователь'), db_index=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name=_('статус'), default="1")
    comment = models.TextField(null=True, blank=True, max_length=10000, verbose_name=_('комментарий администратора'))

    class Meta:
        verbose_name = _('заявка на звонок')
        verbose_name_plural = _('заявки на звонок')

    def __str__(self):
        return f"call request #{self.id} from {self.from_user if self.from_user else _('пользователь удалён')}"
