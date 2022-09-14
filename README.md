# Вступительное задание
Разработан REST API сервис, который позволяет пользователям загружать и обновлять информацию о файлах и папках.
#
Реализованы ендпоинты:
- /imports
- /delete/{id}
- /nodes/{id}
- /updates
- /node/{id}/history
- Документация /docs

### Стек:
- [Docker](https://www.docker.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [sqlalchemy]()


### Deploy
- Клонирование репозитория 
>git clone https://github.com/rmyagkix/my_yandex_disk
- Переходим в дирректорию с проектом 
>cd my_yandex_disk
- Создаем виртуального окружение и активируем его
>python3 -m venv venv 
>source venv/bin/activate
- загрузка и установка необходимых библиотек: 
>pip install -r requirements.txt
- Запуск docker-compose:
> docker-compose -f docker-compose.yaml up -d
- Запуск main файла:
> python main.py 
