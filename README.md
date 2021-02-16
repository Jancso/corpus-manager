# Child Language Acquisition Corpus Manager

Building a child language acquisition corpus is a time-consuming task
since most of the data can only be collected manually. Such corpora often
suffer from 'data problems' such as missing, erroneous or inconsistent data.
Furthermore, building such a corpus is also an organizational challenge
as many people in parallel are working on tasks, requiring appropriate
coordination and synchronization.

The idea to build a web-based corpus manager arose based on these challenges.
Metadata and workflow data had previously been collected in CSVs and shared
over git. Since these do not apply any constraints on the entered data,
we also had a set of scripts which checked those CSVs.
However, those were only run sporadically and therefore data problems tended
to start to accumulate. A web-application, on the other, can
apply validation before data is stored, thereby keeping 'bad' data out of a
database right from the beginning.

The web-app offers the following functionality:
* Grant or revoke access to platform for specific people
* Add metadata for sessions, recordings, participants, etc.
* Export metadata to IMDI
* Assign specific tasks to people such as segmenting, transcribing and glossing
* Post issues and ideas to a forum
* Download a backup of your database

## Run web-application

You can run it in two ways:
* Docker (production)
* Python environment (local)

### Docker (production)
Install Docker first: https://docs.docker.com/get-docker/

Run the following commands (change environment variables and volume paths if needed)
```shell
sudo docker build -t dene .

sudo docker run -it -p 443:8020 \
     -e SECRET_KEY="This_is_the_secret_key_of_Django" \
     -e DJANGO_SUPERUSER_USERNAME=anna_jancso \
     -e DJANGO_SUPERUSER_PASSWORD=This_is_the_admin_password \
     -e DJANGO_SUPERUSER_EMAIL=admin@example.com \
     -e ALLOWED_HOSTS="dene.corpus-manager.ch" \
     -v /home/ubuntu/database:/opt/app/dene/database \
     -v /home/ubuntu/certificates:/opt/app/dene/certificates \
     dene
```

where `/home/ubuntu/database` will contain the database.

where `/home/ubuntu/certificates` has to contain the following certificate files:
* corpus-manager.ch.crt
* corpus-manager.ch.key


### Python environment (local)
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="This_is_the_secret_key_of_Django"
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```