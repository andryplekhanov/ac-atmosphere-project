import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'dj_ac.settings')

app = Celery('dj_ac')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

# заносим таски в очередь
app.conf.beat_schedule = {
    'Parser': {'task': 'app_settings.tasks.get_rate',
               'schedule': crontab(minute='*/1440')},

}

'''
crontab(minute=0, hour='7,11,15,19')


crontab(minute='*/1')                                           Выполняйте каждую минуту.
crontab(minute=0, hour=0)                           Выполняйте ежедневно в полночь.
crontab(minute=0, hour='*/3')                       Выполняйте каждые три часа: в полночь, в 3 часа ночи, в 6 утра, в 9 утра, 
                                                    в полдень, в 3 часа дня, в 6 вечера, в 9 вечера.
crontab(minute=0, hour='0,3,6,9,12,15,18,21')       То же, что и в предыдущем.
crontab(minute='*/15')                              Выполняйте упражнение каждые 15 минут.
crontab(day_of_week='sunday')                       Выполняйте каждую минуту (!) по воскресеньям.
crontab(minute='*', hour='*', day_of_week='sun')    То же, что и в предыдущем.
crontab(minute='*/10', hour='3,17,22', day_of_week='thu,fri')       Выполняйте каждые десять минут, но только между 3-4 утра, 
                                                                    5-6 вечера и 10-11 вечера по четвергам или пятницам.
crontab(minute=0, hour='*/2,*/3')                   Выполняйте каждый четный час и каждый час, кратный трем. 
                                                    Это означает: каждый час, кроме: 1:00, 5:00, 7:00, 11:00, 1:00, 5:00, 7:00, 11:00
crontab(minute=0, hour='*/5')                       Выполняйте час, кратный 5. Это означает, что он запускается в 3 часа дня, 
                                                    а не в 5 вечера (поскольку 3 часа дня равны 24-часовому значению часов “15”, 
                                                    которое делится на 5).
crontab(minute=0, hour='*/3,8-17')                  Выполняйте каждый час, кратный 3, и каждый час в рабочее время (с 8 утра до 5 вечера).
crontab(0, 0, day_of_month='2')                     Выполняйте во второй день каждого месяца.
crontab(0, 0, day_of_month='2-30/2')                Выполняйте каждый четный день.
crontab(0, 0, day_of_month='1-7,15-21')             Выполняйте в первую и третью недели месяца.
crontab(0, 0, day_of_month='11', month_of_year='5') Казните одиннадцатого мая каждого года.
crontab(0, 0, month_of_year='*/3')                  Выполняйте каждый день в первый месяц каждого квартала.
'''
