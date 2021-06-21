#!/bin/sh

echo "Installing python 3..."
yum install -y python3
echo "Python Version Installed: `python3 --version`"

echo "Adding NodeSource repository for NodeJS installation..."
curl –sL https://rpm.nodesource.com/setup_15.x | bash -

echo "Installing NodeJS..."
yum install -y nodejs 
echo "Node Version Installed: `node --version`"

echo "Installing Angular CLI..."
npm install -g @angular/cli 
echo "Angular Version Installed:\n`ng version`"

echo "Installing Nginx..."
yum install -y epel-release
yum install -y nginx 
echo "Nginx Version Installed: `nginx -v`"

cd ./back-end

echo "Creating virtual environment for python packages..."
python3 -m venv venv
echo "Activating virtual environment for package installation..."
source ./venv/bin/activate
echo "Installing necessary python packages..."
pip install -r requirements.txt

echo "Initializing MySQL database..."
python3 db_init.py

echo "Deactivating virtual environment..."
deactivate

echo "Copying Nginx configuration to /etc/nginx/nginx.conf"
cp ../config/nginx.conf /etc/nginx/nginx.conf

echo "Copying Gunicorn system service for Flask backend to /etc/systemd/system/bdmparse.service"
cp ../config/bdmparse.service /etc/systemd/system/bdmparse.service

echo "Copying SSL certificates to /etc/ssl/certs and /etc/ssl/private"
mkdir /etc/ssl/certs
mkdir /etc/ssl/private
cp ../config/nginx-selfsigned.crt /etc/ssl/certs/nginx-selfsigned.crt
cp ../config/nginx-selfsigned.key /etc/ssl/private/nginx-selfsigned.key

cd ../front-end

echo "Installing Angular dependencies..."
npm install

echo "Building Angular project..."
ng build --prod

echo "Elevating privileges to read/execute for Nginx..."
chmod -R 755 ..
chmod og+x /home/admin

echo "Updating firewall to allow http and https traffic..."
firewall-cmd --permanent --zone=public --add-service=http
firewall-cmd --permanent --zone=public --add-service=https
firewall-cmd --reload

echo "Starting and enabling Nginx system service..."
systemctl start nginx
systemctl enable nginx

echo "Starting and enabling firewalld system service..."
systemctl start firewalld
systemctl enable firewalld

echo "Starting and enabling bdmparse system service..."
systemctl start bdmparse
systemctl enable bdmparse
