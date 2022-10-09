#  Foodgram - продуктовый помощник
![workflow](https://github.com/tvs2320/foodgram-project-react/workflows/foodgram_workflow/badge.svg)

## Описание проекта:
Сервис публикации рецептов с подписками на любимых авторов, возможностью добавлять понравившиеся рецепты в список "Избранное", 
возможностью добавлять рецепты по которым будете скоро готовить в "Список покупок", а потом скачивать сводный перечень продуктов на все рецепты из 
"Списка покупок".

## Технологии:
Django
Python
Docker
nginx

## Описание Workflow
##### Workflow состоит из четырёх шагов:
- Проверка кода на соответствие PEP8.
###### Push Docker image to Docker Hub
- Сборка и публикация образа на DockerHub.
###### deploy 
- Автоматический деплой на удаленный сервер при push в главную ветку.
###### send_massage
- Отправка уведомления в телеграм-чат.

## Подготовка и запуск проекта
##### Клонирование репозитория
Склонируйте репозиторий на локальную машину:
```bash
git clone git@github.com:tvs2320/foodgram-project-react.git
```

## Установка на удаленном сервере (Ubuntu):
##### № 1. Выполните вход на свой удаленный сервер
Прежде, чем приступать к работе, необходимо выполнить вход на свой удаленный сервер:
```bash
ssh <USERNAME>@<IP_ADDRESS>
```

##### № 2. Установите docker и docker-compose на удаленный сервер:
Введите команды:
```bash
sudo apt install docker.io 
```

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

##### № 3. Локально отредактируйте файл nginx.conf
Локально отредактируйте файл `infra/nginx.conf` и в строке `server_name` впишите свой IP.

##### № 4. Скопируйте подготовленные файлы из каталога infra:
Скопируйте подготовленные файлы `infra/docker-compose.yml` и `infra/nginx.conf` из вашего проекта на сервер в `home/<ваш_username>/docker-compose.yml` и `home/<ваш_username>/nginx.conf` соответственно.
Введите команду из корневой папки проекта:
```bash
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

##### № 5. Cоздайте .env файл:
На сервере создайте файл `nano .env` и заполните переменные окружения (или создайте этот файл локально и скопируйте файл по аналогии с предыдущим шагом):
```bash
SECRET_KEY=<SECRET_KEY>

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

##### № 6. Добавьте Secrets:
Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<пароль DockerHub>
DOCKER_USERNAME=<имя пользователя DockerHub>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID своего телеграм-аккаунта>
TELEGRAM_TOKEN=<токен вашего бота>
```

##### № 7. После успешной загрузки:
Зайдите на боевой сервер и выполните команды:

###### Выполнить команду docker-compose на удаленном сервере:
```bash
sudo docker-compose up -d --build
```

###### Создать и применить миграции:
```bash
sudo docker-compose exec backend python manage.py makemigrations --noinput
sudo docker-compose exec backend python manage.py migrate --noinput
```
###### Создать суперпользователя Django:
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```
###### Подгрузить статику
```bash
sudo docker-compose exec backend python manage.py collectstatic --noinput 
```
###### Заполнить базу данных:
```bash
sudo docker-compose exec backend python manage.py loaddata fixtures/ingredients.json
```

##### № 8. Проект запущен:
Проект будет доступен по вашему IP-адресу.
