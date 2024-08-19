#!/usr/bin/env python3

##########################################
#                                        #
#      CREATED BY THE PHONEINTEL TEAM    #
#                                        #
##########################################
#                                        #
# ALL INFORMATION IS SOURCED EXCLUSIVELY #
#      FROM OPEN SOURCE AND PUBLIC       #
#               RESOURCES                #
#                                        #
#     THIS NOTICE MUST REMAIN INTACT     #
#   FOR CODE REDISTRIBUTION UNDER THE    #
#           APACHE 2.0 LICENSE           #
#                                        #
##########################################


import hmac
import hashlib
import urllib.parse
import json
import requests
from phoneintel.src.utils.const import IG_KEY


class PhoneIntelInstagram:
    def __init__(self, phone):
        self.url = 'https://i.instagram.com/api/v1/users/lookup/'
        self.ig_sig_key = IG_KEY
        self.sig_key_version = '4'
        if str(phone).startswith("+"):
            phone = phone
        self.phone = phone
        self.out = None
        self.query_instagram()
        
    def signature(self, data):
        return ('ig_sig_key_version=' + self.sig_key_version + '&signed_body=' + 
                hmac.new(self.ig_sig_key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + 
                '.' + urllib.parse.quote_plus(data))

    def data(self):
        return {
            'login_attempt_count': '0',
            'directly_sign_in': 'true',
            'source': 'default',
            'q': str(self.phone),
            'ig_sig_key_version': self.sig_key_version
        }

    def query_instagram(self):
        data = self.signature(json.dumps(self.data()))
        headers = {
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 101.0.0.15.120",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "X-FB-HTTP-Engine": "Liger",
            "Connection": "close"
        }

        try:
            response = requests.post(self.url, headers=headers, data=data)
            response = response.json()
            if "message" in response.keys() and response["message"] == "No users found":
                self.out = False
            else:
                self.out = True
        except:
            self.out = False

    def get(self):
        return self.out
