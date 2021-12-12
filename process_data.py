# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 22:20:28 2021

@author: hanzl
"""

#TODO to change how to get auth
AUTH = '827e8e1a-119c-48e2-af1c-cef81f933a5a'
SASL_PASS = 'h0EsaIyNsFKrejrLmVsJZwOahA+2wgXBbSdHO/jJNyrEJ0p19LV+bdYeD2XR3gRU'
SASL_USER = 'KTIDDULUPUETVKOR'
BOOTSTRAP = ['pkc-4ygn6.europe-west3.gcp.confluent.cloud:9092']
from json import loads
from kafka import KafkaConsumer
import requests
from pymongo import MongoClient



class Mongodatabase ():
    def __init__(self, address: str = 'localhost:27017'):
        self.client = MongoClient('localhost:27017')
        self.db = self.client.catalogue
    def insert_new_product (self, message):
        self.db.products.insert_one(message)
    def find_message_by_id(self, message_id):
        return self.db.products.find_one({'payload.id': message_id})
       
# import logging
# logging.basicConfig(level=logging.DEBUG)

def start_process():
    Mongo = Mongodatabase()
    consumer = KafkaConsumer('catalogue_source',
                             bootstrap_servers=BOOTSTRAP,
                             security_protocol = 'SASL_SSL',
                             sasl_mechanism = 'PLAIN',
                             sasl_plain_username = SASL_USER,
                             sasl_plain_password = SASL_PASS,
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        print(message)
        message = message.value
        if message.get('metadata').get('type') == 'offer':
            offer_id = message.get('payload').get('id')
            if offer_id is not None:
                url = f'http://127.0.0.1:5000/offer-matches/{offer_id}'
                r = requests.get(url =url,  headers={'auth' : AUTH} )
                if r:
                    matching_offers = r.json().get('matching_offers')
                    message_params =  message.get('payload').get('parameters')
                    message['payload']['matching_offers']=[]
                    if len (matching_offers)>0:
                        for matching_offer in matching_offers:
                            joint_params = []
                            differen_params = []
                            matching_offer = Mongo.find_message_by_id(matching_offer)
                            matching_offer_params = matching_offer.get('payload').get('parameters')
                            m_offer_id = matching_offer.get('payload').get('id')
                            for key, val in message_params.items():
                                if (key, val) in matching_offer_params.items():
                                    joint_params.append(key)
                                else:
                                    differen_params.append(key)
                            message['payload']['matching_offers'].append({'m_offer_id':m_offer_id,
                                                                          'joint_params':joint_params,
                                                                          'differen_params':differen_params}) 
        Mongo.insert_new_product(message)
        
start_process()