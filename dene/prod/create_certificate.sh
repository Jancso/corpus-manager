# create CSR (only country code: CH, common name: corpus-manager.ch)
openssl req -new -newkey rsa:2048 -nodes -keyout corpus-manager.ch.key -out corpus-manager.ch.csr
# send content of 'corpus-manager.ch.csr' to CA
# download certificates from CA and upload to server

# copy private key and certificates to proper locations
sudo cp corpus-manager.ch.key /etc/ssl/private/
sudo cp certificate.crt /etc/ssl/certs/
sudo mkdir /etc/apache2/ssl.crt/
sudo cp ca.crt /etc/apache2/ssl.crt/

# set SSLCertificateFile, SSLCertificateKeyFile and SSLCertificateChainFile in
# default-ssl.conf (https)
cp default-ssl.conf /etc/apache2/sites-available/

# add Redirect permanent to 000-default.conf (http)
cp 000-default.conf /etc/apache2/sites-available/

sudo a2enmod ssl
sudo a2enmod headers
sudo a2ensite default-ssl
sudo systemctl restart apache2
