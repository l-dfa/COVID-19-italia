# filename utils.py
#   a module of utilities

import configparser
import csv
import sys

from datetime import datetime
from pathlib import Path

import paramiko
import pandas as pd


FILE_CONFIG = './utils.conf'
config = configparser.ConfigParser()   # a config parser
config.read(Path(FILE_CONFIG))

DIR_ARTICLE  = './article'
DIR_TEMPLATE = './template'
DIR_IMG      = './images'    # images directory for infection in Italy
DIR_DATA     = './data'      # data directory
DIR_WIMG     = './world'     # images directory for worldwide infection


# enable debug mode
ENABLE_DEBUG = config['debug']['ENABLE_DEBUG'] in ['true', 'True']

# global variables to send data to production host
HOST = config['production']['HOST']
USER = config['production']['USER']
PKEY = config['production']['PKEY']
TO   = 5.0                   # timeout 5 sec
ENABLE_PRODUCTION = config['production']['ENABLE_PRODUCTION'] in ['true', 'True']

D_FMT   = '%Y-%m-%d'              # format date as yyyy-mm-dd
D_FMT2  = '%d/%m/%Y'              # format date as dd/mm/yyyy
DT_FMT  = '%Y-%m-%dT%H:%M:%S'     # format datetime as yyyy-mm-ddThh:mm:ss
DT_FMT2 = '%Y-%m-%d %H:%M:%S'     # format datetime as yyyy-mm-dd hh:mm:ss

# global variables to send data to ldfa filesystem
ENABLE_LDFA = config['ldfa']['ENABLE_LDFA'] in ['true', 'True']
DIR_ROOT_LDFA = Path(config['ldfa']['DIR_ROOT_LDFA'])

DIR_LDFA = {
    'articles':     DIR_ROOT_LDFA / 'articles', 
    'data_italy':   DIR_ROOT_LDFA / 'media/data/204', 
    'data_world':   DIR_ROOT_LDFA / 'media/data/210', 
    'images_italy': DIR_ROOT_LDFA / 'media/images/204', 
    'images_world': DIR_ROOT_LDFA / 'media/images/210', 
}

# paths to production server
DIR_ROOT_PRODUCTION = config['production']['DIR_ROOT_PRODUCTION']
DIR_PRODUCTION = {
    'articles':     DIR_ROOT_PRODUCTION + '/' + 'articles', 
    'data_italy':   DIR_ROOT_PRODUCTION + '/' + 'media/data/204', 
    'data_world':   DIR_ROOT_PRODUCTION + '/' + 'media/data/210', 
    'images_italy': DIR_ROOT_PRODUCTION + '/' + 'media/images/204', 
    'images_world': DIR_ROOT_PRODUCTION + '/' + 'media/images/210', 
}

# START columns of pandas dataframe from csv and excel files

# Italian national trend csv
# example:
#     data,stato,ricoverati_con_sintomi,terapia_intensiva,totale_ospedalizzati,isolamento_domiciliare,totale_attualmente_positivi,nuovi_attualmente_positivi,dimessi_guariti,deceduti,totale_casi,tamponi,note_it,note_en
#     2020-02-24T18:00:00,ITA,101,26,127,94,221,221,1,7,229,4324,,
# we do not import these fields: note_it, note_en
COLUMNS_ITALY = {
    'it': {
        'data': 'data',
        'stato': 'stato',
        'ricoverati_con_sintomi': 'ricoverati con sintomi',
        'terapia_intensiva': 'terapia intensiva',
        'totale_ospedalizzati': 'ospedalizzati',
        'isolamento_domiciliare': 'isolamento domiciliare',
        'totale_positivi': 'positivi',
        'variazione_totale_positivi': 'variazione positivi',
        'nuovi_positivi': 'nuovi positivi',
        'dimessi_guariti': 'guariti',
        'deceduti': 'deceduti',
        'totale_casi': 'totale casi',
        'tamponi': 'tamponi',
    },
    'en': {
        'data': 'date',
        'stato': 'state',
        'ricoverati_con_sintomi': 'hospitalized',
        'terapia_intensiva': 'intensive care',
        'totale_ospedalizzati': 'overall hospit.',
        'isolamento_domiciliare': 'quarantine at home',
        'totale_positivi': 'positives',
        'variazione_totale_positivi': 'change of positives',
        'nuovi_positivi': 'new positives',
        'dimessi_guariti': 'healed',
        'deceduti': 'deceased',
        'totale_casi': 'overall cases',
        'tamponi': 'swab',
    },
}

# Italian regional trends csv
# example:
#    data,stato,codice_regione,denominazione_regione,lat,long,ricoverati_con_sintomi,terapia_intensiva,totale_ospedalizzati,isolamento_domiciliare,totale_attualmente_positivi,nuovi_attualmente_positivi,dimessi_guariti,deceduti,totale_casi,tamponi,note_it,note_en
#    2020-02-24T18:00:00,ITA,13,Abruzzo,42.35122196,13.39843823,0,0,0,0,0,0,0,0,0,5,,
# we do not import these fields: lat, long, note_it, note_en
COLUMNS_RITALY = {
    'it': {
        'data': 'data',
        'stato': 'stato',
        'codice_regione': 'codice_regione',
        'denominazione_regione': 'denominazione_regione',
        'ricoverati_con_sintomi': 'ricoverati_con_sintomi',
        'terapia_intensiva': 'terapia_intensiva',
        'totale_ospedalizzati': 'ospedalizzati',
        'isolamento_domiciliare': 'isolamento_domiciliare',
        'totale_positivi': 'positivi',
        'variazione_totale_positivi': 'variazione_positivi',
        'nuovi_positivi': 'nuovi_positivi',
        'dimessi_guariti': 'guariti',
        'deceduti': 'deceduti',
        'totale_casi': 'totale_casi',
        'tamponi': 'tamponi',
    },
    'en': {
        'data': 'date',
        'stato': 'state',
        'codice_regione': 'region id.',
        'denominazione_regione': 'region name',
        'ricoverati_con_sintomi': 'hospitalized',
        'terapia_intensiva': 'intensive care',
        'totale_ospedalizzati': 'overall hospit.',
        'isolamento_domiciliare': 'quarantine at home',
        'totale_positivi': 'positives',
        'variazione_totale_positivi': 'change of positives',
        'nuovi_positivi': 'new positives',
        'dimessi_guariti': 'healed',
        'deceduti': 'deceased',
        'totale_casi': 'overall cases',
        'tamponi': 'swab',
    },
}


# world trend csv
# example (beware of row index in 1st position)
#     ,dateRep,day,month,year,cases,deaths,countriesAndTerritories,geoId
#     0,30/03/2020,30,3,2020,8,1,Afghanistan,AF
# 
# dataframe for world data, after shape_world
#     #   Column     Non-Null Count  Dtype
#     0   date       5841 non-null   object   this is a datetime.date yyyy-mm-dd
#     1   day        5841 non-null   int64
#     2   month      5841 non-null   int64
#     3   year       5841 non-null   int64
#     4   cases      5841 non-null   int64
#     5   deaths     5841 non-null   int64
#     6   countries  5841 non-null   object
#     7   geoid      5835 non-null   object
# + ldfa @ 2020-04-09 get in the country population

COLUMNS_WORLD = {
    'it': {
        'dateRep': 'data',
        'day': 'giorno',
        'month': 'mese',
        'year': 'anno',
        'cases': 'casi',
        'deaths': 'decessi',
        'countriesAndTerritories': 'paesi',
        'geoId': 'geoid',
        #'popData2018': 'popolazione',
        'popData2019': 'popolazione',
    },
    'en': {
        'dateRep': 'date',
        'day': 'day',
        'month': 'month',
        'year': 'year',
        'cases': 'cases',
        'deaths': 'death',
        'countriesAndTerritories': 'country',
        'geoId': 'geoid',
        #'popData2018': 'population',
        'popData2019': 'population',
    }
}
# END   columns of pandas dataframe from csv and excel files


def load_df(fname, opener, cols=None, encoding='utf-8'):
    '''
    create a dataframe from a file
    
    params:
      - fname       str or Path - file to read
      - opener      pandas method - usually pd.excel() or pd.read_csv()
      - cols        dict - a collection of columns names and their translation in a certain language
                           i.e. {col1: col1_lang, col2: col2_lang, ...}
      - encoding    str - encoder to use reading dataframe
    
    return df a dataframe
    '''

    # get data, rename columns, drop duplicates, ignore nulls
    df = opener(fname, encoding=encoding)
    
    # drop all columns that are not present in cols
    if not cols is None:
        df_cols = list(df.columns)
        for col in df_cols:
            if not col in cols.keys():
                df.drop(col, axis=1, inplace=True)
    
    #df.rename(columns=cols, inplace=True) #ATTENZIONE
    
    ashape = df.shape
    df.drop_duplicates(inplace=True)
    if df.shape!=ashape:
        print(f'duplicates dropped: {ashape[0]-df.shape[0]}')
    return df

def shape_data(df, cols, keyerr=True):
    '''
    '''
    if not keyerr:
        for col in df.columns:
            if col not in cols:
                cols.pop(col)
    df.rename(columns=cols, inplace=True)
    return df
    

def to_production(source_data_dir, dest_data_dir, source_image_dir, dest_image_dir, data_files, image_files):
    '''
    copy files from the project filesystem to production server
    
    params:
      - source_data_dir,   str - from directory of data files
      - dest_data_dir,     str - to directory of data files
      - source_image_dir,  str - from directory of image files
      - dest_image_dir,    str - to directory of image files
      - data_files,        list - file names of data
      - image_files        list - file names of images
    
    return None
    '''
    private_key = paramiko.RSAKey.from_private_key_file(PKEY)
    with paramiko.SSHClient() as ssh_client:
        ssh_client.load_host_keys('known_hosts')
        #ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOST, username=USER, pkey=private_key, timeout=TO, allow_agent=False, look_for_keys=False)
        sftp_client = ssh_client.open_sftp()
        
        # world data to production directory
        for afile in data_files:
            sftp_client.put(Path(source_data_dir) / afile, dest_data_dir +'/'+ afile)  #local, remote
        
        # world images to production directory
        for afile in image_files:
            sftp_client.put(Path(source_image_dir) / afile, dest_image_dir +'/'+ afile)  #local, remote
        
    return

def to_rst_table(df_str):
    lines = df_str.split('\n')
    lines = ['  '+line for line in lines]
    df_str = '\n'.join(lines)
    df_str = df_str.replace('_', ' ')
    return df_str
