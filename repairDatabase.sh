#!/bin/bash
sudo service mongod stop
sudo -u mongod mongod --repair --dbpath /data/db/
sudo service mongod status

