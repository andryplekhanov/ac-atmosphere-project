# AC-Atmosphere telegram-bot with Django admin

Telegram-бот на AIOgram с админкой Django для продажи кондиционеров и оказания услуг.
- **Language** (язык): Russian
- **Author** (Автор): [Андрей Плеханов](https://t.me/andryplekhanov)


- **Демонстрация работы программы:** [смотреть видео >>](https://youtu.be/HbrVmbOxhO4)


## Возможности бота
Бот реагирует на команды:
- **/start** - Запустить бота
- **/menu** - Товары и услуги - навигационное многоуровневое меню: категории и подкатегории товаров с возможностью посмотреть детальную информацию о товаре/услуге и оформить заказ.
- **/call** - Заказать звонок
- **/mess** - Написать нам сообщение
- **/about** - О нас - информация о компании: настраивается в админке Django
- **/help** - Вывести справку

## Запуск
- скачайте проект
- файл ".env.dist" переименуйте в ".env" и пропишите необходимые настройки
- выполните команды (должен быть запущен Docker):
```bash
# установить плагин для Docker (после установки перезагрузить машину)
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions

# смонтировать контейнер:
docker-compose build

# запустить контейнер:
docker-compose up -d

# применить миграции:
docker-compose exec web sh -c "python manage.py migrate"

# создать суперпользователя:
docker-compose exec web sh -c "python manage.py createsuperuser"

# загрузить фикстуры в БД:
docker-compose exec web sh -c "python manage.py loaddata fixtures/db.json"
```

Теперь можно перейти на http://0.0.0.0:8000/admin/ и войти в админку под суперпользователем

## Просмотр логов

Для просмотра логов необходимо:
- перейти в Grafana: http://0.0.0.0:3000
- перейти Configuration > Add data source > Loki
- задать url: http://loki:3100
- сохранить: Save & test
- перейти в раздел Explore
- в Label filters выбрать нужный раздел
- нажать Run query
