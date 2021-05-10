#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
import json
import requests
from sys import exit
import xmlrpc.client


def updateLoopiaIP(domains, subdomains, username, password):
    logger.debug('Updating IP')
    try:
        ip = requests.get('https://ifconfig.me') # could use https://icanhazip.com, http://checkip.dyndns.org
        ip = ip.text
        logger.debug('Current IP: ' + ip)
    except Exception as e:
        logger.critical('Current IP retrieval error')
        logger.critical(e)
        exit()

    domain_server_url = 'https://api.loopia.se/RPCSERV' 
    try:
        client = xmlrpc.client.ServerProxy(domain_server_url, encoding = 'utf-8')
        for d, sd in zip(domains, subdomains):
            old_record_obj = client.getZoneRecords(username, password, d, sd)

            record_id = old_record_obj[0]['record_id'] 
            old_ip = old_record_obj[0]['rdata']

            if old_ip == ip:
                logger.debug('IP already matches')
            else:
                record_obj = {'type': 'A', 'ttl': 300, 'priority': 0, 'rdata': ip, 'record_id': record_id}
                response = client.updateZoneRecord(username, password, d, sd, record_obj)
                logger.debug('IP update Loopia response: '+ response)
    except Exception as e:
        logger.critical('Loopia IP update failed')
        logger.critical(e)
        exit()


if __name__ == '__main__':
    # logging
    log_handler = RotatingFileHandler('updateLoopiaIPLog.log', maxBytes=20000, backupCount=2)
    log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    log_handler.setFormatter(log_formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_handler)

    # config
    try:
        with open('updateLoopiaIPConfig.json') as file:
            config = json.load(file)
    except (IOError, FileNotFoundError, json.JSONDecodeError):
        logger.critical('Config file not OK')
        exit()
    try:
        domains = config['domains']
        subdomains = config['subdomains']
        username = config['username']
        password = config['password']
    except Exception as e:
        logger.critical('Config file inaccurate')
        exit()
        
    if type(domains) is not list:
        domains = [domains]
    if type(subdomains) is not list:
        subdomains = [subdomains]

    updateLoopiaIP(domains, subdomains, username, password)  
