# django-aiogram-template

Шаблон для создания Telegram-бота на AIOgram с админкой Django.


## Запуск
- скачайте проект
- файл ".env.dist" переименуйте в ".env" и пропишите необходимые настройки
- выполните команды (должен быть запущен Docker):
```bash
# смонтировать контейнер:
docker-compose build

# запустить контейнер:
docker-compose up -d

# остановить контейнер:
docker-compose stop

# если в код были внесены изменения, необходимо заново смонтировать контейнер
```


## Миграции
Команды выполняются при запущенном контейнере
```bash
# создание миграций:
docker-compose exec web sh -c "python manage.py makemigrations"

# применение миграций:
docker-compose exec web sh -c "python manage.py migrate"

# создание суперпользователя:
docker-compose exec web sh -c "python manage.py createsuperuser"

# загрузка фикстур в БД:
docker-compose exec web sh -c "python manage.py loaddata fixtures/db.json"
```

Теперь можно перейти на http://0.0.0.0:8000/admin/ и войти в админку под суперпользователем
