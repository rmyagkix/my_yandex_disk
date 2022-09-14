# Вступительное задание
Разработан REST API сервис, который позволяет пользователям загружать и обновлять информацию о файлах и папках.
###Реализованы endpoints:
- /imports
- /delete/{id}
- /nodes/{id}
- /updates
- /node/{id}/history
- /docs 
#
### Стек:
- [Docker](https://www.docker.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [sqlalchemy](https://www.sqlalchemy.org/)

#
### Deploy
- Клонирование репозитория 
```
git clone https://github.com/rmyagkix/my_yandex_disk
```
- Переход в дирректорию с проектом 
```
cd my_yandex_disk
```
- Создание виртуального окружение и его активация
```
python3 -m venv venv
source venv/bin/activate
```
- Загрузка и установка необходимых библиотек: 
```
pip install -r requirements.txt
```
- Запуск docker-compose:
```
docker-compose -f docker-compose.yaml up -d
```
- Копирование <code>first-task.service</code> в нужную дирректорию:
```
sudo cp first-task.service /etc/systemd/system/
```
- Запуск службы:
```
sudo systemctl daemon-reload
sudo systemctl enable --now first-task.service
```
- Проверка работоспособности:
```
sudo systemctl status first-task.service

● first-task.service
     Loaded: loaded (/etc/systemd/system/first-task.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2022-09-14 21:40:24 UTC; 24min ago
   Main PID: 552 (python3)
      Tasks: 4 (limit: 75)
     Memory: 102.8M
     CGroup: /system.slice/first-task.service
             ├─552 /home/ubuntu/my_yandex_disk/venv/bin/python3 /home/ubuntu/my_yandex_disk/main.py
             ├─597 /home/ubuntu/my_yandex_disk/venv/bin/python3 -c from multiprocessing.resource_tracker import main;main(5)
             └─598 /home/ubuntu/my_yandex_disk/venv/bin/python3 -c from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=6, pipe_handle=8) --multiprocessing->
Sep 14 21:40:24 instrumental-2050 systemd[1]: Started first-task.service.
Sep 14 21:40:26 instrumental-2050 python3[552]: INFO:     Will watch for changes in these directories: ['/home/ubuntu/my_yandex_disk']
Sep 14 21:40:26 instrumental-2050 python3[552]: INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
Sep 14 21:40:26 instrumental-2050 python3[552]: INFO:     Started reloader process [552] using WatchFiles
Sep 14 21:40:27 instrumental-2050 python3[598]: INFO:     Started server process [598]
Sep 14 21:40:27 instrumental-2050 python3[598]: INFO:     Waiting for application startup.
Sep 14 21:40:27 instrumental-2050 python3[598]: INFO:     Application startup complete.
```