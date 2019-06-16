#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
import configparser
import requests
from sys import exit
import xmlrpc.client


def updateLoopiaIP(domain, uname, passw):
    logger.debug('Updating IP')
    try:
        ip = requests.get('https://ifconfig.me') # could use https://icanhazip.com, http://checkip.dyndns.org
        ip = ip.text
        logger.debug('Current IP: ' + ip)
    except Exception as e:
        logger.critical('Current IP retrieval error')
        logger.critical(e)
        exit()

    try:
        username = uname
        password = passw
        domain_server_url = 'https://api.loopia.se/RPCSERV' 

        domain = domain
        subdomain = '@'

        client = xmlrpc.client.ServerProxy(domain_server_url, encoding = 'utf-8')

        old_record_obj = client.getZoneRecords(username, password, domain, subdomain)

        record_id = old_record_obj[0]['record_id'] 
        old_ip = old_record_obj[0]['rdata']

        if old_ip == ip:
            logger.debug('IP already matches')
        else:
            record_obj = {'type': 'A', 'ttl': 300, 'priority': 0, 'rdata': ip, 'record_id': record_id}
            response = client.updateZoneRecord(username, password, domain, subdomain, record_obj)
            logger.debug('IP update Loopia response: '+ response)
    except Exception as e:
        logger.critical('Loopia IP update failed')
        logger.critical(e)
        exit()


if __name__ == '__main__':
    # logging
    log_handler = RotatingFileHandler('Log.log', maxBytes=20000, backupCount=2)
    log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    log_handler.setFormatter(log_formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

    # config
    config = configparser.ConfigParser()
    config.read('config.cfg')
    try:
        domain = config['credentials']['domain']
        uname = config['credentials']['uname']
        passw = config['credentials']['passw']
    except Exception as e:
        logger.critical('Config file inaccurate')
        exit()

    updateLoopiaIP(domain, uname, passw)  

