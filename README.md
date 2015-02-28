cmcweb
======

CMC web application based on Django.
The current Django version used for this project is 1.6.4.


How to Install & run a local instance 
=====================================
** This is based on a Ubuntu server and you will run this project with virtualenv and MySQL server.


Install Virtualenv and PIP

> apt-get install python-pip python-virtualenv


Install GIT 

> sudo apt-get install git


Install MySQL

> sudo apt-get install mysql-server
> sudo apt-get install libmysqlclient-dev

Install python dev library

> sudo apt-get install python-dev



Setup virtualenv and project Under /home/admin

> mkdir PYENV 


Under /home/admin/PYENV

> virtualenv cmcweb_prj


Under /home/admin/PYENV/cmcweb_prj
> git clone https://github.com/coolkang/cmcweb.git


Activate virtualenv
> source bin/activate

Install necessary packages for the project

> pip install -r requirements.txt


** You need below part to run this project with an Apache web server.

Install Apache

> sudo apt-get install apache2
> sudo apt-get install libapache2-mod-wsgi

Create a log file folder & change a permission of the folder

> mkdir /home/admin/PYENV/cmcweb_prj/cmcweb/cmcprj/LOGS/
> chmod -R 777 ~/PYENV/cmcweb_prj/cmcweb/cmcprj/LOGS


Create a static files folder

> sudo mkdir /var/www/hadiye.org


Run collectstatic command to copy static files to the above static file folder.
WITH virtualenv activated

> python manage.py collectstatic --settings=cmcprj.settings.production

Copy httpd.conf AS hadiye.org.conf  into /etc/apache2/sites-available folder
And run the below command

> sudo a2ensite hadiye.org.conf
> sudo service apache2 reload

