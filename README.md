# worknotes-server

* dependency:
  - apt install python-dev
  - apt install virtualenv

* config setup:
  - modify etc/config.py
  - modify worknote.ini

* mysql setup:
  - CREATE USER 'm2x'@'localhost' IDENTIFIED BY 'm2x12345';
  - GRANT ALL ON private_server.* TO 'm2x'@'localhost';

* run server
  - source setup.sh
