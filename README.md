# Описание

Это тестовое задание предназначено для проверки знаний построения связей в БД и умения правильно строить запросы без ошибок N+1.

# Требования

Время выполнения: ~ 8 часов для junior уровня
Срок сдачи: в течении 4 дней

# Используемые технологии

Django 4.2
Django REST framework
SQLite


# Решение

Для решения этого задания была построена следующая архитектура:
Сущность продукта: хранит информацию о продукте, включая название, описание и владельца.
Сущность урока: хранит информацию об уроке, включая название, ссылку на видео и длительность просмотра.
Сущность доступа: хранит информацию о доступе пользователя к продукту.
Сущность просмотра: хранит информацию о просмотре урока пользователем, включая время просмотра и статус (просмотрено/не просмотрено).
Для реализации API были использованы следующие методы Django REST framework:

filter(): для фильтрации результатов запроса.
annotate():** для добавления дополнительной информации к результатам запроса.
order_by():** для сортировки результатов запроса.



# Для запуска приложения необходимо выполнить следующие действия:

Создать виртуальное окружение:
python3 -m venv venv
Активировать виртуальное окружение:
source venv/bin/activate
Установить зависимости:
pip install -r requirements.txt
Запустить приложение:
python manage.py runserver