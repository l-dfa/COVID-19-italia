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

import histogram as h
import plot      as p
import table     as t
import utils     as u


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

def make_article(template, national_data, regions_data, lang='it', title=''):
    #set_width_in_fields(plot_data)
    
    #get article template
    with open(Path(u.DIR_TEMPLATE) / template, 'r') as f:
        template_from_file = f.read()
    dt = datetime.now()
    
    #v  = u.load_data(Path(u.DIR_DATA) / general_file)    # national trend
    #sd = t.shape_data(v)
    sd = t.shape_data(national_data, cut=['stato'])
    rst_it = t.make_table(sd, p.FIELDS, lang, title)
    
    #v  = u.load_data(Path(u.DIR_DATA) / regions_file)    # regional trend
    #sd = t.shape_data(v)
    #rst_region = t.make_table(sd, h.FIELDS, lang)
    sd = t.shape_data(regions_data)
    rst_region = t.make_table(sd, h.FIELDS, lang)
    
    d = dict()
    d['MODIFIED']    = dt.strftime(u.DT_FMT)
    d['UPDATED']     = dt.date().strftime(DATE_FMT)
    d['DATA_TABLE']  = rst_it
    d['RDATA_TABLE'] = rst_region
    
    tmpl = Template(template_from_file)
    article = tmpl.safe_substitute(d)
    
    with open(Path(u.DIR_ARTICLE) / template, 'w') as f:
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
    fnames = map(lambda fn, ext: os.path.splitext(fn)[0]+'.'+ext, [p.FN, p.FN, h.FN, h.FN], ['png', 'en.png', 'png', 'en.png'])
    for fname in fnames:
        copyfile(Path(u.DIR_IMG) / fname, u.DIR_LDFA['images_italy'] / fname)


def to_production(adate):
    private_key = paramiko.RSAKey.from_private_key_file(u.PKEY)
    with paramiko.SSHClient() as ssh_client:
        ssh_client.load_host_keys('known_hosts')
        #ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=u.HOST, username=u.USER, pkey=private_key, timeout=u.TO, allow_agent=False, look_for_keys=False)
        sftp_client = ssh_client.open_sftp()
        
        # italy data to production server
        for csv_fname in SOURCES.keys():
            sftp_client.put(Path(u.DIR_DATA) / csv_fname, u.DIR_PRODUCTION['data_italy'] +'/'+ csv_fname)  #local, remote
        
        # italy images to production server
        fnames = map(lambda fn, ext: os.path.splitext(fn)[0]+'.'+ext, [p.FN, p.FN, h.FN, h.FN], ['png', 'en.png', 'png', 'en.png'])
        for fname in fnames:
            sftp_client.put(Path(u.DIR_WIMG) / fnames, u.DIR_PRODUCTION['images_italy'] +'/'+ fnames)  #local, remote

    #ssh_client.close()
    return

    
def main(afile=p.FN):
    if BACKUP:
        backup()
    
    if DOWNLOAD:
        dt = datetime.now()
        rc = get_data(dt.date().strftime(DATEURL_FMT))
        if rc == -1:
            print("error downloading today's data")
            sys.exit(-1)
    
    v  = u.load_data(Path(u.DIR_DATA) / afile)
    sd = p.shape_data(v)
    
    p.make_plot(sd, afile, 'it')
    p.make_plot(sd, afile, 'en')
    
    v2  = u.load_data(Path(u.DIR_DATA) / h.FN)
    sd2 = h.shape_data(v2)
    h.save_data(sd2)
    #print(sd2)
    #sys.exit
    
    h.make_histogram(sd2, h.FN, 'it')
    h.make_histogram(sd2, h.FN, 'en')
    
    article = make_article(FN_IT_TEMPLATE, sd, sd2, 'it', t.TAB_TITLE)
    article = make_article(FN_EN_TEMPLATE, sd, sd2, 'en', t.TAB_EN_TITLE)

    to_ldfa()


if __name__=='__main__':
    arguments()
    main(p.FN)
