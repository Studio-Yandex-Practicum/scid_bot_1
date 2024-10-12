# SCID Telegram Bot

## Описание
Телеграм-бот для агентства разработки SCID, служащий проводником по продуктам и услугам компании. 

### Технологии:
- Python
- FastAPI
- aiogram
- SQLAlchemy
- PostgreSQL
- Docker

## Подготовка и запуск проекта с DockerHub

Клонировать репозиторий и перейти в него в командной строке:
```shell
git clone git@github.com:Studio-Yandex-Practicum/scid_bot_1.git
```
```shell
cd scid_bot_1
```

Скопировать файл `.env.example` в файл `.env` в указанных каталогах:

```shell
copy .env.example .env
```
```shell
cd bot && copy .env.example .env
```
```shell
cd ..\fastapi_app && copy .env.example .env
```
```shell
cd ..\test_bot && copy .env.example .env
```

Запустить проект в контейнерах Docker:
```shell
cd .. && docker compose -f docker-compose.yml up
```

## Команда разработки
**Александр Пастух**  
**Андрей Горбаненко**  
**Андрей Егоров**  
**Владимир Бондаренко**  
**Петр Горюнов**  
**Яков Аустер**  
