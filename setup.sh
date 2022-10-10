service mysql start
virtualenv venv --python=python2.7
source venv/bin/activate
pip install uwsgi
pip install flask
pip install flask_login
pip install mysql-python
pip install torndb
pip install python-dateutil
pip install concurrent-log-handler
mkdir -p var logs
uwsgi worknotes.ini
