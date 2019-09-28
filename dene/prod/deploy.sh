sudo apt-get update
sudo apt-get upgrade
sudo apt-get install apache2 apache2-dev python3-venv libapache2-mod-wsgi-py3
git clone https://github.com/Jancso/dene-webapp.git
sudo chown www-data:www-data dene-webapp/
cd dene-webapp
sudo chown -R www-data media/
python3 -m venv venv
source venv/bin/activate
pip install wheel mod_wsgi django pillow
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
deactivate
mkdir prod_static
sudo chown www-data:www-data db.sqlite3
sudo cp apache2.conf /etc/apache2/apache2.conf
sudo systemctl restart apache2.service
