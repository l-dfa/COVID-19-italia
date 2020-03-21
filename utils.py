# filename utils.py
#   a module of utilities

import csv
from pathlib import Path
import sys

DIR_ARTICLE  = './article'
DIR_TEMPLATE = './template'
DIR_IMG      = './images'    # images directory for infection in Italy
DIR_DATA     = './data'      # data directory
DIR_WIMG     = './world'     # images directory for worldwide infection

HOST = '151.11.50.179'
USER = 'root'
PKEY = r'C:\Bin\PuTTYPortable\Data\settings\hostek2\id_rsa'
TO   = 5.0


D_FMT = '%Y-%m-%d'               # format date as yyyy-mm-dd
DT_FMT = '%Y-%m-%d %H:%M:%S'     # format date as yyyy-mm-dd hh:mm:ss

DIR_ROOT_LDFA = Path('/Dati/Studio/Sviluppi/ldfa/contents')
DIR_LDFA = {
    'articles':     DIR_ROOT_LDFA / 'articles', 
    'data_italy':   DIR_ROOT_LDFA / 'media/data/204', 
    'data_world':   DIR_ROOT_LDFA / 'media/data/210', 
    'images_italy': DIR_ROOT_LDFA / 'media/images/204', 
    'images_world': DIR_ROOT_LDFA / 'media/images/210', 
}

DIR_ROOT_PRODUCTION = '/usr/share/nginx/html/ldfa/rstsite/contents'
DIR_PRODUCTION = {
    'articles':     DIR_ROOT_PRODUCTION + '/' + 'articles', 
    'data_italy':   DIR_ROOT_PRODUCTION + '/' + 'media/data/204', 
    'data_world':   DIR_ROOT_PRODUCTION + '/' + 'media/data/210', 
    'images_italy': DIR_ROOT_PRODUCTION + '/' + 'media/images/204', 
    'images_world': DIR_ROOT_PRODUCTION + '/' + 'media/images/210', 
}

def get_date(v):
    '''get date list from list of dicts
    
       param: v        list of dicts - [{fld1: val11, fld2:val12, ...},
                                       {fld1: val21, fld2:val22, ...},
                                       ... ]
       return: a list of date
       
       Note:
         - key 'data' identifies the date to extract (it's in italian language)
         - being a list, the returned value has the usual index operations;
           e.g. to get the last 4 days: get_date(v)[-4:]
    '''
    l = list( set( [row['data'] for row in v] ) )
    return sorted(l)
    
def load_data(afile):
    '''load a csv file as list of dicts
    
       param: afile     str or FILE - whatever is good to 'open'
       
       return a list of dicts: [{fld1: val11, fld2: val12, ...},
                                {fld1: val21, fld2: val22, ...},
                                ... ]
    '''
    with open(afile, 'r') as f:
        v = list(csv.DictReader(f, delimiter=','))
    return v
    
def save_data(v, afile):
    '''save a list of dicts as csv file
    
       param:
         - v         list of dicts
         - afile     str or FILE - whatever is good to 'open'
       
       return 0 or raise exception
    '''
    with open(afile, 'w', newline='') as f:
        fieldnames = list(v[0].keys())
        w = csv.DictWriter(f, delimiter=',', fieldnames=fieldnames)
        first = {fname: fname for fname in fieldnames}
        w.writerow(first)
        for row in v:
            w.writerow(row)
    return 0
