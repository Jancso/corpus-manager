# Run web-application

You can run it in two ways:
* Docker
* conventional with a python environment

### Docker (local or production)
Install Docker first: https://docs.docker.com/get-docker/

Run the following commands (change port, username, password and mail if needed)
```shell
docker build -t dene .

docker run -it -p 80:8020 \
     -e DJANGO_SUPERUSER_USERNAME=admin \
     -e DJANGO_SUPERUSER_PASSWORD=sekret1 \
     -e DJANGO_SUPERUSER_EMAIL=admin@example.com \
     dene
```

### Conventional (local only)
```
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```