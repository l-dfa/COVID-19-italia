# filename world.py
#    plot time series of overall cases for 10 most hitted nations

help = '''python world.py [--date=yyyy-mm-dd] [-d:true|false]
options:
  --date   plot at indicated date (default: today)
  -d       download data from Internet (default: True)
'''

import getopt
import sys
import os
import urllib.request

from pathlib  import Path
from datetime import datetime, date
from shutil   import copyfile
from string   import Template

import matplotlib.pyplot as plt
import pandas            as pd
import paramiko

import utils             as u

# START section: BEFORE to use these variables, INSERT DATE
TITLE10 = 'Covid-19: temporal trend of total number of cases from {};\n10 countries with the highest total'
TITLE09 = 'Covid-19: temporal trend of total number of cases from {};\n9 countries with the highest total, excluding China'

SOURCE = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{}.xlsx'
FNAME  = 'covid19-worldwide-{}.xlsx'
# END   section: BEFORE to use these variables, INSERT DATE

WORLD_FILE = u.DIR_DATA + '/' + 'covid19-worldwide-2020-03-18.xls'   # test file

FN_IT_TEMPLATE  = '210_coronavirus_mondo.rst'
FN_EN_TEMPLATE  = '211_coronavirus_mondo.en.rst'
ADATE = date.today().strftime(u.D_FMT)

DOWNLOAD = True

COLUMNS = {
'DateRep': 'date',
'Day': 'day',
'Month': 'month',
'Year': 'year',
'Cases': 'cases',
'Deaths': 'death',
'Countries and territories': 'country',
'GeoId': 'id',
}


def usage():
    print(help)


def arguments():
    global DOWNLOAD
    global ADATE
    #import pdb; pdb.set_trace()       # DEBUG
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:", ["date=", "help", "download="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--download"):
            DOWNLOAD = True if a=="True" or a=="true" else False
        elif o == "--date":
            ADATE = a[:]
        else:
            assert False, "unhandled option"


def get_data(adate):
    #import pdb; pdb.set_trace()       # DEBUG

    # make test for data available
    url = SOURCE.format(adate)
    try:
        with urllib.request.urlopen(url) as response:
           pass
    except:
        return -1
    fn = FNAME.format(adate)
    # download data
    with urllib.request.urlopen(url) as response:
       from_web = response.read()
    with open(Path(u.DIR_DATA) / fn, 'wb') as f:
        f.write(from_web)
    return 0
    
def get_countries(df, n):
    '''get n top countries by total of cases
       
       params:
         - df         pandas dataframe - date, cases, country
         - n          int - how many countries to list
         
       return a list of country names
    '''
    # list nations (get series of countries)
    #   df:   country
    #      0  Afganistan
    #      1  Albania
    #      ...
    countries = pd.DataFrame(df['country'])
    countries.drop_duplicates(inplace=True)
    #print(countries.head())
    
    # total cases by nation
    #   df:      country   total_cases
    #      0  Afganistan           22
    #      1  Albania              55
    #      ...
    totals =[]
    for acountry in countries['country']:
        totals.append(df[(df['country']==acountry)]['cases'].sum())
    countries['total_cases'] = totals
    #print(countries.head())
    
    # here select n nations with bigger total_cases
    countries.sort_values(['total_cases'], inplace=True, ascending=False)
    countries = countries.head(n)
    return list(countries['country'])
    
    
def elaborate(adate):

    # get data, rename columns, drop duplicates, ignore nulls
    fname = FNAME.format(adate)
    df = pd.read_excel(Path(u.DIR_DATA) / fname)
    df.rename(columns=COLUMNS, inplace=True)
    df2 = df.drop_duplicates()
    if df2.shape!=df.shape:
        print(f'duplicates dropped: {df.shape[0]-df2.shape[0]}')
    
    # get 10 most hitted countries
    countries = get_countries(df, 10)
    
    # graph of time series of previous 10 nations
    # from df          date  ...  cases  ...                   country  id  |  to sdfx   country     China  France  Germany  Iran  ...  Spain  Switzerland  United_Kingdom  United_States_of_America
    #       1060 2020-03-18  ...     33  ...                     China  CN  |            date                                      ...
    #       1061 2020-03-17  ...    110  ...                     China  CN  |            2019-12-31     27       0        0     0  ...      0            0               0                         0
    #       1062 2020-03-16  ...     25  ...                     China  CN  |            ...
    #       ...         ...  ...    ...  ...                       ...  ..  |            2020-03-17    110    1210     1174  1053  ...   1438            0             152                       887
    #       5441 2020-01-01  ...      0  ...  United_States_of_America  US  |            2020-03-18     33    1097     1144  1178  ...   1987          450             407                      1766
    #       5442 2019-12-31  ...      0  ...  United_States_of_America  US  |
    # hereafter prepare data to plot top 10 countries
    sdf1 = df[(df['country'].isin(countries))]
    sdf11 = sdf1.pivot(index='date', columns='country', values='cases')
    sdf11.sort_values(['date'], inplace=True)
    sdf11 = sdf11.cumsum()
    sdf11.to_csv(Path(u.DIR_DATA) / (os.path.splitext(fname)[0]+'.csv'))
    sdf11 = sdf11.iloc[14:]                   # with china, out first 14 days
    adate = sdf11.index[0]                    # the remaining 1st date
    # plot and draw to file
    ax = sdf11.plot(title=TITLE10.format(adate.strftime(u.D_FMT)),
                    figsize=(9,7))
    ax.grid(linestyle='--', axis='both')
    plot_fname1 = os.path.splitext(fname)[0]+'.wchina.en.png'
    plt.savefig(Path(u.DIR_WIMG) / plot_fname1, format='png') # show to file
    plt.close()
    
    # hereafter we select top 9 countries by total_cases excluding china
    sdf2 = df[(df['country'].isin(countries[1:]))]
    sdf21 = sdf2.pivot(index='date', columns='country', values='cases')
    sdf21.sort_values(['date'], inplace=True)
    sdf21 = sdf21.cumsum()
    sdf21 = sdf21.iloc[51:]                    # without china, get out first 51 days
    adate = sdf21.index[0]                     # the remaining 1st date
    # plot and draw to file
    ax = sdf21.plot(title=TITLE09.format(adate.strftime(u.D_FMT)),
                    figsize=(9,7))
    ax.grid(linestyle='--', axis='both')
    plot_fname2 = os.path.splitext(fname)[0]+'.en.png'
    plt.savefig(Path(u.DIR_WIMG) / plot_fname2, format='png') # show to file
    
    #plt.show()
    
    # does plot EU as a federation?
    return 0
    
    
def make_article(template, adate):
    
    #get article template
    with open(Path(u.DIR_TEMPLATE) / template, 'r') as f:
        template_from_file = f.read()
    dt = datetime.now()
    
    # prepare variable contents
    d = dict()
    d['MODIFIED'] = dt.strftime(u.DT_FMT)
    d['UPDATED']  = adate
    
    # merge template with var.contents
    tmpl = Template(template_from_file)
    article = tmpl.safe_substitute(d)
    
    # save it
    with open(Path(u.DIR_ARTICLE) / template, 'w') as f:
        f.write(article)
        
    return article


def to_ldfa(adate):
    # world articles to ldfa directory
    copyfile(Path(u.DIR_ARTICLE) / FN_IT_TEMPLATE, u.DIR_LDFA['articles'] / FN_IT_TEMPLATE)
    copyfile(Path(u.DIR_ARTICLE) / FN_EN_TEMPLATE, u.DIR_LDFA['articles'] / FN_EN_TEMPLATE)
    
    # world data to ldfa directory
    fname = FNAME.format(adate)                                 # covid19-worldwide-{}.xlsx   with adate
    copyfile(Path(u.DIR_DATA) / fname, u.DIR_LDFA['data_world'] / fname)
    csv_fname = os.path.splitext(fname)[0]+'.csv'               # covid19-worldwide-{}.csv    with adate
    copyfile(Path(u.DIR_DATA) / csv_fname, u.DIR_LDFA['data_world'] / csv_fname)
    
    # world images to ldfa directory
    plot_fname1 = os.path.splitext(fname)[0]+'.wchina.en.png'   # covid19-worldwide-{}wchina.en.png with adate
    copyfile(Path(u.DIR_WIMG) / plot_fname1, u.DIR_LDFA['images_world'] / plot_fname1)
    plot_fname2 = os.path.splitext(fname)[0]+'.en.png'          # covid19-worldwide-{}.en.png       with adate
    copyfile(Path(u.DIR_WIMG) / plot_fname2, u.DIR_LDFA['images_world'] / plot_fname2)
    return
    

def to_production(adate):
    private_key = paramiko.RSAKey.from_private_key_file(u.PKEY)
    with paramiko.SSHClient() as ssh_client:
        ssh_client.load_host_keys('known_hosts')
        #ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=u.HOST, username=u.USER, pkey=private_key, timeout=u.TO, allow_agent=False, look_for_keys=False)
        sftp_client = ssh_client.open_sftp()
        
        # world data to production directory
        fname = FNAME.format(adate)                                 # covid19-worldwide-{}.xlsx   with adate. WARN: DO NOT REWRITE it's used again
        sftp_client.put(Path(u.DIR_DATA) / fname, u.DIR_PRODUCTION['data_world'] +'/'+ fname)  #local, remote
        csv_fname = os.path.splitext(fname)[0]+'.csv'               # covid19-worldwide-{}.csv    with adate
        sftp_client.put(Path(u.DIR_DATA) / csv_fname, u.DIR_PRODUCTION['data_world'] +'/'+ csv_fname)  #local, remote
        
        # world images to production directory
        plot_fname = os.path.splitext(fname)[0]+'.wchina.en.png'   # covid19-worldwide-{}wchina.en.png with adate
        sftp_client.put(Path(u.DIR_WIMG) / plot_fname, u.DIR_PRODUCTION['images_world'] +'/'+ plot_fname)  #local, remote
        plot_fname = os.path.splitext(fname)[0]+'.en.png'          # covid19-worldwide-{}.en.png       with adate
        sftp_client.put(Path(u.DIR_WIMG) / plot_fname, u.DIR_PRODUCTION['images_world'] +'/'+ plot_fname)  #local, remote
    
    #ssh_client.close()
    return

def main(adate):
    if DOWNLOAD:
        get_data(adate)
    
    elaborate(adate)
    
    make_article(FN_IT_TEMPLATE, adate)
    make_article(FN_EN_TEMPLATE, adate)
    
    to_ldfa(adate)
    to_production(adate)
    


if __name__=='__main__':
    arguments()
    main(ADATE)

