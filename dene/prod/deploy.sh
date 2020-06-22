# Create instance
# Image: Ubuntu 18.04

# set host in dene/prod/settings.py: ALLOWED_HOSTS

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install apache2 apache2-dev python3-venv libapache2-mod-wsgi-py3 python3-dev

git clone https://github.com/Jancso/dene-webapp.git
cd dene-webapp

cp dene/prod/settings.py dene/

mkdir prod_static

python3 -m venv venv
source venv/bin/activate
pip install wheel mod_wsgi
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
deactivate

sudo chown www-data:www-data db.sqlite3
sudo chown -R www-data media/
sudo chown www-data:www-data ../dene-webapp/

sed -i 's,${HOME},'"${HOME}"',g' dene/prod/apache2.conf
sudo cp dene/prod/apache2.conf /etc/apache2/apache2.conf
# apachectl configtest
sudo systemctl restart apache2.service

# use SSL
cd dene/prod
sh create_certificate.sh

# for heavy tasks such as imports
cd ../..
nohup python manage.py process_tasks &
