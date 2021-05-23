#!/bin/sh
python3 www.py --bind http://0.0.0.0:8090/ --bind 'https://0.0.0.0:8443/?certfile=/etc/letsencrypt/live/www.florianbest.de/cert.pem&keyfile=/etc/letsencrypt/live/www.florianbest.de/privkey.pem' -c domains.cfg -n -l /dev/stderr $@
