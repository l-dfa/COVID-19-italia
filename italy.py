# filename update.py
#   update article 204 using a template and modules 
#     - plot.py
#     - data.py

help = '''python update.py [-f: file] [-d: true] [-b: true]
options:
  -f       file is data file name
  -d       download data from Internet (default True)
  -b       backup data before download it from Internet (default True)
'''

import getopt
import os
import statistics as stats
import sys
import urllib.request

from datetime import datetime, date
from pathlib import Path
from shutil import copyfile
from string import Template

import matplotlib.pyplot as plt
import pandas   as pd

import histogram as h
import plot      as p
#import table     as t
import utils     as u

TAB_TITLE    = "Serie storiche dell'infezione covid-2019 per l'Italia; fonte: Ministero della Salute, tramite Protezione Civile"
TAB_EN_TITLE = "Time series of covid-2019 infection for Italy; source: Ministry of Health, by Civil Protection"

DIR_ROOT_BACKUP = './backup'
FN_IT_TEMPLATE  = '204_coronavirus_italia.rst'
FN_EN_TEMPLATE  = '205_coronavirus_italia.en.rst'
DATE_FMT        = '%d-%m-%Y'
DATEURL_FMT     = '%Y%m%d'
SOURCE_TEST = 'https://github.com/pcm-dpc/COVID-19/blob/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-{:s}.csv'
SOURCES         = {
    'dpc-covid19-ita-andamento-nazionale.csv': 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv',
    'dpc-covid19-ita-regioni.csv':             'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv',
    'dpc-covid19-ita-province.csv':            'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv',
}
NUM_RDAYS = 7

DOWNLOAD = True
BACKUP   = True


def usage():
    print(help)


def arguments():
    global FN
    global DOWNLOAD
    global BACKUP
    #import pdb; pdb.set_trace()       # DEBUG
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:d:b:", ["help", "file=", "download=", "backup="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-f", "--file"):
            FN = a
        elif o in ("-d", "--download"):
            DOWNLOAD = True if a=="True" or a=="true" else False
        elif o in ("-b", "--backup"):
            BACKUP = True if a=="True" or a=="true" else False
        else:
            assert False, "unhandled option"


def backup():
    d = date.today()
    #d = date(1999, 10, 10)                                        # DEBUG
    dir_backup = Path(DIR_ROOT_BACKUP) / d.strftime(DATEURL_FMT)   # ./backup/yyyymmdd
    if not dir_backup.exists():                                    # create it
        dir_backup.mkdir()
    dir_data_backup = dir_backup / Path(u.DIR_DATA).name             # ./backup/yyyymmdd/data
    if not dir_data_backup.exists():                               # create it
        dir_data_backup.mkdir()
    for fn in SOURCES.keys():
        try:
            data_backup = dir_data_backup / fn                             # ./backup/yyyymmdd/data/dpc-covid19-ita-andamento-nazionale.csv
            if not data_backup.exists():                                   # create it
                copyfile(Path(u.DIR_DATA) / fn, dir_data_backup / fn)
        except:
            print(f'backup "{fn}" fallito')


def get_data(adate):
    # make test for data available
    url = SOURCE_TEST.format(adate)
    try:
        with urllib.request.urlopen(url) as response:
           pass
    except:
        return -1
    
    # download data
    for fn, url in SOURCES.items():
        with urllib.request.urlopen(url) as response:
           from_web = response.read()
        with open(Path(u.DIR_DATA) / fn, 'wb') as f:
            f.write(from_web)
    return 0

def shape_national_data(df, lang='it', drop=[]):
    columns = dict(u.COLUMNS_ITALY[lang])
    df2 = df.copy(deep=True)
    for col in drop:
        if col in df.columns:
            df2 = df2.drop(col, 1)
            columns.pop(col, None)     #del key of value col if exists; ignore if it is not existent
    df2 = df2.rename(columns=columns)
    return df2

def shape_regional_data(df, lang='it', drop=[]):
    columns = dict(u.COLUMNS_RITALY[lang])
    df2 = df.copy(deep=True)
    for col in drop:
        if col in df.columns:
            df2 = df2.drop(col, 1)
            columns.pop(col, None)     #del key of value col if exists; ignore if it is not existent
    series_of_dates = df2['data'].drop_duplicates().sort_values()[-NUM_RDAYS:]
    df2 = df2[df2['data'].isin(series_of_dates)]
    df2 = df2.sort_values(['denominazione_regione', 'data'])
    list_of_regions = h.get_regions_name(df, h.get_regions(df))
    
    # calculating change of healed
    aseries = pd.Series(dtype='int64')
    for region in list_of_regions:
        rdf = df2[df2['denominazione_regione']==region].iloc[-NUM_RDAYS:]
        s = rdf['dimessi_guariti'] - rdf['dimessi_guariti'].shift(1) 
        aseries = pd.concat([aseries, s])
    #import pdb; pdb.set_trace()
    df2['variazione_guariti'] = aseries
    
    # calculating change of deceased
    aseries = pd.Series(dtype='int64')
    for region in list_of_regions:
        rdf = df2[df2['denominazione_regione']==region].iloc[-NUM_RDAYS:]
        s = rdf['deceduti'] - rdf['deceduti'].shift(1) 
        aseries = pd.concat([aseries, s])
    #import pdb; pdb.set_trace()
    df2['variazione_deceduti'] = aseries
    #- ldfa,2020-03-31 now data from Protezione Civile has this columns
    #df2['nuovi_positivi'] = df2['nuovi_attualmente_positivi'] + df2['variazione_guariti'] + df2['variazione_deceduti']
    df2['nuovi_positivi'] = df['nuovi_positivi']
    
    if lang == 'en':
        columns['variazione_guariti'] = 'change_of_healed'
        columns['variazione_deceduti'] = 'change_of_deaths'
        columns['nuovi_positivi'] = 'new_positives'
    df2 = df2.rename(columns=columns)
    return df2

def to_rst_table(df_str):
    lines = df_str.split('\n')
    lines = ['  '+line for line in lines]
    df_str = '\n'.join(lines)
    df_str = df_str.replace('_', ' ')
    return df_str

def make_article(template, national_data, regional_data, lang='it', title=''):
    '''
    Params:
      - template             str - filename of template to use
      - national_data        pandas dataframe - of national trend
      - regions data         pandas dataframe - 
      - lang                 'it' or 'en'
      - title                str
    '''
    #set_width_in_fields(plot_data)
    
    #get article template
    with open(Path(u.DIR_TEMPLATE) / template, 'r') as f:
        template_from_file = f.read()

    dt = datetime.now()
    
    # national data
    df2 = shape_national_data(national_data,
                              lang,
                              drop=['stato',
                                    'ricoverati_con_sintomi',
                                    'terapia_intensiva',
                                    'tamponi',
                                    'note_it',
                                    'note_en']
                             )

    # national data, last day
    df2_last = df2.iloc[[-1], :]
    rst_it_last = df2_last.to_csv(index=False)
    rst_it_last = to_rst_table(rst_it_last)

    # national data, all days
    rst_it = df2.to_csv(index=False)
    rst_it = to_rst_table(rst_it)

    # regional data, last seven days every region
    rdf2 = shape_regional_data(regional_data,
                              lang,
                              drop=['stato',
                                    'codice_regione',
                                    'ricoverati_con_sintomi',
                                    'terapia_intensiva',
                                    'tamponi',]
                             )

    #import pdb; pdb.set_trace()
    data_col = 'data' if lang == 'it' else 'date'
    last_day = rdf2[data_col].max()
    rdf2_last = rdf2[rdf2[data_col]==last_day]

    if lang == 'it':
        columns = [
             'data',
            'denominazione_regione',
            'ospedalizzati',
            'isolamento_domiciliare',
            'positivi',
            'variazione_positivi',
            'nuovi_positivi',
            'guariti',
            'deceduti',
            'totale_casi',
        ]
    else:
        columns = [
        'date',
        'region name',
        'overall hospit.',
        'quarantine at home',
        'positives',
        'change of positives',
        'new_positives',
        'healed',
        'deceased',
        'overall cases',
        ]
    
    rst_region_last = rdf2_last.to_csv(index=False, columns=columns)
    rst_region_last = to_rst_table(rst_region_last)

    # regional data
    rst_region = rdf2.to_csv(index=False, columns=columns)
    rst_region = to_rst_table(rst_region)
    
    d = dict()
    d['MODIFIED']    = dt.strftime(u.DT_FMT2)
    d['UPDATED']     = dt.date().strftime(DATE_FMT)
    d['DATA_TABLE_LAST']  = rst_it_last
    d['DATA_TABLE']  = rst_it
    d['RDATA_TABLE_LAST'] = rst_region_last
    d['RDATA_TABLE'] = rst_region
    
    tmpl = Template(template_from_file)
    article = tmpl.safe_substitute(d)
    
    with open(Path(u.DIR_ARTICLE) / template, 'w', newline='') as f:
        f.write(article)
        
    return article


def to_ldfa():
    # italy articles to ldfa directory 
    copyfile(Path(u.DIR_ARTICLE) / FN_IT_TEMPLATE, u.DIR_LDFA['articles'] / FN_IT_TEMPLATE)
    copyfile(Path(u.DIR_ARTICLE) / FN_EN_TEMPLATE, u.DIR_LDFA['articles'] / FN_EN_TEMPLATE)
    
    # italy data to ldfa directory
    for csv_fname in SOURCES.keys():
        copyfile(Path(u.DIR_DATA) / csv_fname, u.DIR_LDFA['data_italy'] / csv_fname)
    
    # italy images to ldfa directory
    fnames = map(lambda fn, ext: os.path.splitext(fn)[0]+'.'+ext,
                 [p.FN, p.FN, h.FN, h.FN, h.FN, h.FN, p.FN, p.FN],
                 ['png', 'en.png', 'png', 'en.png', 'most_hitted.png', 'most_hitted.en.png', 'nuovi_positivi.png', 'nuovi_positivi.en.png'])
    for fname in fnames:
        copyfile(Path(u.DIR_IMG) / fname, u.DIR_LDFA['images_italy'] / fname)


def to_production():
    
    #import pdb; pdb.set_trace()
    
    # italy data to production server
    data_files = list(SOURCES.keys())
    # italy images to production server
    image_files = map(lambda fn, ext: os.path.splitext(fn)[0]+'.'+ext, 
                      [p.FN, p.FN, h.FN, h.FN, h.FN, h.FN, p.FN, p.FN],
                      ['png', 'en.png', 'png', 'en.png', 'most_hitted.png', 'most_hitted.en.png', 'nuovi_positivi.png', 'nuovi_positivi.en.png'])
    
    u.to_production(u.DIR_DATA, u.DIR_PRODUCTION['data_italy'], u.DIR_IMG, u.DIR_PRODUCTION['images_italy'], data_files, image_files)  #local, remote
        
    #ssh_client.close()
    return

    
def main(afile=p.FN):
    # ATTENZIONE RIMETTERE IN LINEA LE SEGUENTI
    if BACKUP:
        backup()
    
    if DOWNLOAD:
        dt = datetime.now()
        rc = get_data(dt.date().strftime(DATEURL_FMT))
        if rc == -1:
            print("error downloading today's data")
            sys.exit(-1)
           
    #import pdb; pdb.set_trace()
    
    #df = pd.read_csv(Path(u.DIR_DATA) / afile)
    df = u.load_df(Path(u.DIR_DATA) / afile, pd.read_csv, u.COLUMNS_ITALY['it'])
    
    df = p.shape_data(df)
    p.make_plot(df, afile, 'it')
    p.make_plot(df, afile, 'en')
    # FINE ATTENZIONE

    p.make_national(df, 'nuovi_positivi', afile, xlabel='data', ylabel='numero giornaliero di nuovi casi', title=f'Covid-19: andamento temporale giornaliero di nuovi positivi (nazionale)', lang = 'it' )
    p.make_national(df, 'nuovi_positivi', afile, xlabel='date', ylabel='daily number of new cases', title=f'Covid-19: time trend of daily (national) new cases', lang = 'en' )
    
    rdf = u.load_df(Path(u.DIR_DATA) / h.FN, pd.read_csv, u.COLUMNS_RITALY['it'])
    rdf = h.shape_data(rdf)
    
    #p.make_rplot(rdf)
    p.make_rplot(rdf, h.FN, xlabel='data', ylabel='numero totale di casi', title=f'Covid-19: andamento temporale per le {p.N_MOST_HITTED} regioni più colpite', lang = 'it' )
    p.make_rplot(rdf, h.FN, xlabel='date', ylabel='total number of cases', title=f'Covid-19: temporal trend for the {p.N_MOST_HITTED} most hitted regions', lang = 'en' )

    h.make_histogram(rdf, h.FN, 'it')
    h.make_histogram(rdf, h.FN, 'en')
    
    article = make_article(FN_IT_TEMPLATE, df, rdf, 'it', TAB_TITLE)
    article = make_article(FN_EN_TEMPLATE, df, rdf, 'en', TAB_EN_TITLE)
    
    # ATTENZIONE RIMETTERE IN LINEA LE SEGUENTI
    if u.ENABLE_LDFA:
        to_ldfa()
    if u.ENABLE_PRODUCTION:
        to_production()


if __name__=='__main__':
    arguments()
    main(p.FN)
