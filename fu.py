# filename fu.py
# a test program to upload a file (name means file upload)

#import getopt
#import sys
#import os
#import urllib.request

import configparser
from pathlib import Path

import requests

FILE_CONFIG = './utils.conf'
config = configparser.ConfigParser()   # a config parser
config.read(Path(FILE_CONFIG))

ARTICLES = config['fu']['ARTICLES'].split(',')
URLL     = config['fu']['URLL']
URL      = config['fu']['URL']
AUTH     = tuple(config['fu']['AUTH'].split(','))
ARTICLE_PATH = './article'

def main():
    with requests.Session() as s:
        lg = s.get(URL)                                            # article get
        csrf_token = lg.cookies['csrftoken']                       #     csrf
        login_data = {'csrfmiddlewaretoken': csrf_token,
                      'username': AUTH[0],
                      'password': AUTH[1],
                      'next': '/blog/load-article'}
        rl = s.post(URLL, data=login_data)                         # posting to login (NOT article: weird, isn't it?). it switches to load-article AND ...
        csrf_token = rl.cookies['csrftoken']                       # ... it CHANGES csrf
        
        #print('login status: {}'.format(rl.status_code))
        #print('---------')
        #print(rl.text)
        
        load_article_data = {'csrfmiddlewaretoken': csrf_token, }
        for article in ARTICLES:
            files = {'article': open(ARTICLE_PATH + '/' + article, 'rb')}  # the field name is article, not file
            ru = s.post(URL, files=files, data=load_article_data)  
        
        #print('upload status: {}', format(ru.status_code))
        #print('---------')
        #print(ru.text)

if __name__=='__main__':
    main()