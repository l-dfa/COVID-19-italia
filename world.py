# filename world.py
#    plot time series of overall cases for 10 most hitted nations
#    by Coronavirus Covid-19 outbreak
# 2020-03-27 - ECDC has changed data format from xlsx to csv, and URL to get it. 
#              program updated
#            - USA passes China as total cases

help = '''python world.py [--date=yyyy-mm-gg] [-d:true|false]
options:
  --date   plot at indicated date (default: today; beware of format)
  -d       download data from Internet (default: True)
  -p       copy results to production (default: True)
'''

import getopt
import os
import sys
import urllib.request

from pathlib  import Path
from datetime import datetime, date
from shutil   import copyfile
from string   import Template

import matplotlib.pyplot as plt
import pandas            as pd
#import paramiko

import utils             as u

# START section: BEFORE to use these variables, INSERT DATE
TITLE10 = 'Covid-19: temporal trend of total number of cases from {};\n10 countries with the highest total'
TITLE09 = 'Covid-19: temporal trend of total number of cases from {};\nfrom the 2nd to the 10th countries with the highest total'
# END   section: BEFORE to use these variables, INSERT DATE

# out from 27 march 2020
#SOURCE = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{}.xlsx'
#FNAME  = 'covid19-worldwide-{}.xlsx'
#WORLD_FILE = u.DIR_DATA + '/' + 'covid19-worldwide-2020-03-18.xls'   # test file

# from 27 march 2020 this is the new url, without date; and data are in csv format
SOURCE = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
FNAME  = 'covid19-worldwide-{}.csv'
# END   section: BEFORE to use these variables, INSERT DATE

FN_IT_TEMPLATE  = '210_coronavirus_mondo.rst'
FN_EN_TEMPLATE  = '211_coronavirus_mondo.en.rst'
ADATE = date.today().strftime(u.D_FMT)

DOWNLOAD   = True          # if true get data from Internet
PRODUCTION = True          # if true copy data to ldfa filesystem and production server



def usage():
    print(help)


def arguments():
    '''
    Analize command line arguments
    
    global variables:
      - DOWNLOAD              bool - True to  download data from Internet
      - ADATE                 date - the update date
      - PRODUCTION            bool - True to copy results to filesystem and to production server
    '''
    global DOWNLOAD
    global ADATE
    global PRODUCTION
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:p:", ["date=", "help", "download=", "production="])
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
        elif o in ("-p", "--production"):
            PRODUCTION = True if a=="True" or a=="true" else False
        elif o == "--date":
            # check string date format (yyyy-mm-dd)
            ADATE = datetime.strptime(a[:], u.D_FMT).date().strftime(u.D_FMT)
        else:
            assert False, "unhandled option"

    
def get_data(adate):
    '''
    download data from internet and save it to file
    
    params: adate          str - the update date
    
    return df if success, or None if adate is not present in df
      - df             pandas dataframe - as u.COLUMNS_WORLD['en']
      
    collateral effects: if success, save df as csv file
    '''
    
    # load datafram from internet
    url = SOURCE
    fn = FNAME.format(adate)
    df = u.load_df(url, pd.read_csv)
    
    # test for udated data available
    check_date = datetime.strptime(adate, u.D_FMT).date().strftime(u.D_FMT2)
    bflag = df['dateRep'].str.contains(check_date).any()
    if bflag:
        df.to_csv(Path(u.DIR_DATA) / fn)
    else:
        df = None

    return df
    
    
def world_shape(df):
    '''
    models dataframe to our needs
    
    params: df        pandas dataframe - df to model
    
    return df         pandas dataframe - the modeled dataframe
    '''
    #df['date'] = df['date'].map(lambda x: x.date()) # from datetime to date
    df['dateRep'] = df['dateRep'].map(lambda x: datetime.strptime(x, u.D_FMT2).date()) # from str to date
    df.loc[(df['countriesAndTerritories']=='CANADA'), 'countriesAndTerritories'] = 'Canada'
    df.rename(columns=u.COLUMNS_WORLD['en'], inplace=True)
    return df


def get_countries(df):
    '''
    list country names in decreasing order by total cases
    
    params:
      - df         pandas dataframe - date, cases, country
      
    return a list of country names 
    '''
    # list nations (get series of countries)
    #   df:   country
    #      0  Afganistan
    #      1  Albania
    #      ...
    countries = pd.DataFrame(df['country'])
    countries.drop_duplicates(inplace=True)
    
    # total cases by nation
    #   df:      country   total_cases
    #      0  Afganistan           22
    #      1  Albania              55
    #      ...
    totals =[]
    for acountry in countries['country']:
        totals.append(df[(df['country']==acountry)]['cases'].sum())
    countries['total_cases'] = totals
    
    # sorting countries by ytotal cases
    countries.sort_values(['total_cases'], inplace=True, ascending=False)
    return list(countries['country'])
    
def world_get_sum_on_last_day(df):
    '''
    create a new dataframe with total cases and some other data
    
    params: df             pandas dataframe - input df
    
    return a new df with  columns:
      - 'date',         date
      - 'day',          int
      - 'month',        int
      - 'year',         int
      - 'cases',        int
      - 'death',        int
      - 'death/cases',  float
      - 'country',      str
      - 'geoid'         str
    '''
    l = []           # will be: [[date, sum, country], [date, sum, country], ...]
    countries = df['country'].drop_duplicates()   # get a copy
    
    for country in countries:
        country_df = df.loc[df['country']==country].copy()
        the_cases = country_df['cases'].sum()
        the_deaths = country_df['death'].sum()
        the_date = country_df['date'].max()
        the_day = country_df['day'].max()
        the_month = country_df['month'].max()
        the_year = country_df['year'].max()
        geoid = country_df['geoid'].max()
        if the_cases == 0:
            deathly = None
        else:
            deathly = the_deaths / the_cases
        l.append((the_date, the_day, the_month, the_year, the_cases, the_deaths, deathly, country[:], geoid))
        
    df2 = pd.DataFrame(l, columns=['date', 'day', 'month', 'year', 'cases', 'death', 'death/cases', 'country', 'geoid'])
    df2 = df2.sort_values('cases', ascending=False)
    return df2    
    
def elaborate(df, adate):
    '''
    plot two line graphs
    
    params: 
      - df            pandas dataframe -
      - adate         date - date to build filename to save graphs
    
    return always 0
    
    side effects: plot two graphs and save as png files
    '''
    
    fname = FNAME.format(adate)
    
    # get 10 most hitted countries
    countries = get_countries(df)[:10]
    colors=['tab:blue',
            'tab:orange',
            'tab:green',
            'tab:red',
            'tab:purple',
            'tab:brown',
            'tab:pink',
            'tab:gray',
            'tab:olive',
            'tab:cyan']
    
    # graph of time series of previous 10 nations
    # from df          date  ...  cases  ...                   country  id  |  to sdfx   country     China  France  Germany  Iran  ...
    #       1060 2020-03-18  ...     33  ...                     China  CN  |            date                                      ...
    #       1061 2020-03-17  ...    110  ...                     China  CN  |            2019-12-31     27       0        0     0  ...
    #       1062 2020-03-16  ...     25  ...                     China  CN  |            ...
    #       ...         ...  ...    ...  ...                       ...  ..  |            2020-03-17    110    1210     1174  1053  ...
    #       5441 2020-01-01  ...      0  ...  United_States_of_America  US  |            2020-03-18     33    1097     1144  1178  ...
    #       5442 2019-12-31  ...      0  ...  United_States_of_America  US  |
    # hereafter prepare data to plot top 10 countries
    sdf1 = df[(df['country'].isin(countries))]
    
    # WARNING: next instruction is ok because dates are the same for these nations
    #    BUT some countries have less dates then others; IF one of this nations 
    #    enters in the top ten this instruction will raise exception
    sdf11 = sdf1.pivot(index='date', columns='country', values='cases')
    sdf11.sort_values(['date'], inplace=True)
    sdf11 = sdf11.cumsum()
    sdf11.to_csv(Path(u.DIR_DATA) / (os.path.splitext(fname)[0]+'_pivot.csv'))
    sdf11 = sdf11.iloc[14:]                   # 1st graph: out first 14 days
    adate = sdf11.index[0]                    # the remaining 1st date
    # plot and draw to file
    ax = sdf11.plot(title=TITLE10.format(adate.strftime(u.D_FMT)),
                    figsize=(9,7),
                    color=colors
                    )
    ax.grid(linestyle='--', axis='both')
    plot_fname1 = os.path.splitext(fname)[0]+'.wchina.en.png'
    plt.savefig(Path(u.DIR_WIMG) / plot_fname1, format='png') # show to file
    plt.close()
    
    # hereafter using the same countries we show after the 51 days
    countries = get_countries(df)[1:10]

    sdf2 = df[(df['country'].isin(countries))]
    # WARNING: see previous WARNING
    sdf21 = sdf2.pivot(index='date', columns='country', values='cases')
    sdf21.sort_values(['date'], inplace=True)
    sdf21 = sdf21.cumsum()
    sdf21 = sdf21.iloc[51:]                    # 2nd graph: get out first 51 days
    adate = sdf21.index[0]                     # the remaining 1st date
    # plot and draw to file
    ax = sdf21.plot(title=TITLE09.format(adate.strftime(u.D_FMT)),
                    figsize=(9,7),
                    color=colors,
                    rot=60
                    )
    ax.grid(linestyle='--', axis='both')
    fig = ax.get_figure()
    fig.subplots_adjust(bottom=0.2)

    plot_fname2 = os.path.splitext(fname)[0]+'.en.png'
    plt.savefig(Path(u.DIR_WIMG) / plot_fname2, format='png') # show to file
    
    #plt.show()
    
    # do we plot EU as a federation?
    return 0
    
    
def make_article(template, adate, df):
    '''
    istantiate an article merging a template with actual data
    
    params: 
      - template              str or Path - to a filename containing the template to use
      - adate                 date - to use as update date
      - df                    pandas dataframe - to use as source of data
      
    return article            str - the composed article
    
    side effects: save article as file
    '''
    #get article template
    with open(template, 'r') as f:
        template_from_file = f.read()
    dt = datetime.now()
    
    # get last day situation of 10 hitted nations
    countries = get_countries(df)[:10]
    df2 = world_get_sum_on_last_day(df)[:20]
    columns = ['date', 'cases', 'death', 'death/cases', 'country' ]
    data_table = df2.to_csv(columns=columns,index=False, float_format = '%.5f')
    lines = data_table.split('\n')
    lines = ['  '+line for line in lines]
    data_table = '\n'.join(lines)
    data_table = data_table.replace('_', ' ')

    # prepare variable contents
    d = dict()
    d['MODIFIED'] = dt.strftime(u.DT_FMT2)
    d['UPDATED']  = adate
    d['DATA_TABLE']  = data_table
    
    # merge template with var.contents
    tmpl = Template(template_from_file)
    article = tmpl.safe_substitute(d)
    
    # save it
    with open(Path(u.DIR_ARTICLE) / os.path.split(template)[1], 'w', newline='') as f:
        f.write(article)
        
    return article


def to_ldfa(adate):
    '''
    copy files from the project filesystem to articles filesystem
    
    params: adate          date - the update date
    
    return None
    '''
    # world articles to ldfa directory
    copyfile(Path(u.DIR_ARTICLE) / FN_IT_TEMPLATE, u.DIR_LDFA['articles'] / FN_IT_TEMPLATE)
    copyfile(Path(u.DIR_ARTICLE) / FN_EN_TEMPLATE, u.DIR_LDFA['articles'] / FN_EN_TEMPLATE)
    
    # world data to ldfa directory
    fname = FNAME.format(adate)                                 # covid19-worldwide-{}.csv   with adate
    copyfile(Path(u.DIR_DATA) / fname, u.DIR_LDFA['data_world'] / fname)
    csv_fname = os.path.splitext(fname)[0]+'_pivot.csv'               # covid19-worldwide-{}_pivot.csv    with adate
    copyfile(Path(u.DIR_DATA) / csv_fname, u.DIR_LDFA['data_world'] / csv_fname)
    
    # world images to ldfa directory
    plot_fname1 = os.path.splitext(fname)[0]+'.wchina.en.png'   # covid19-worldwide-{}wchina.en.png with adate
    copyfile(Path(u.DIR_WIMG) / plot_fname1, u.DIR_LDFA['images_world'] / plot_fname1)
    plot_fname2 = os.path.splitext(fname)[0]+'.en.png'          # covid19-worldwide-{}.en.png       with adate
    copyfile(Path(u.DIR_WIMG) / plot_fname2, u.DIR_LDFA['images_world'] / plot_fname2)
    return
    

def to_production(adate):
    '''
    copy files from the project filesystem to production server
    
    params: adate          date - the update date
    
    return None
    '''
    
    fname = FNAME.format(adate)                   # covid19-worldwide-{}.csv   with adate
    
    # list of data files
    data_files = []
    data_files.append(fname[:])
    
    image_files = []
    image_files.append(os.path.splitext(fname)[0]+'.wchina.en.png'[:])    # covid19-worldwide-{}.wchina.en.png with adate
    image_files.append(os.path.splitext(fname)[0]+'.en.png'[:])           # covid19-worldwide-{}.en.png with adate
    
    u.to_production(u.DIR_DATA, u.DIR_PRODUCTION['data_world'], u.DIR_WIMG, u.DIR_PRODUCTION['images_world'], data_files, image_files)
    
    return

def main(adate):
    #import pdb; pdb.set_trace()
    # get data
    if DOWNLOAD:
        df = get_data(adate)
        if type(df) == type(None):        # we cannot do: df == None because if df is dataframe it raises ValueError
            print('data from Internet not updated. run interrupted')
            sys.exit(1)
    else:
        df = u.load_df(u.DIR_DATA+'/'+FNAME.format(adate), pd.read_csv, u.COLUMNS_WORLD['en'], encoding='cp1250')
    df = world_shape(df)
    
    # make two graphs
    elaborate(df, adate)
    
    # make articles
    make_article(u.DIR_TEMPLATE+'/'+FN_IT_TEMPLATE, adate, df)
    make_article(u.DIR_TEMPLATE+'/'+FN_EN_TEMPLATE, adate, df)
    
    # copy results to ldfa filesystem and to production
    if PRODUCTION:
        to_ldfa(adate)
        to_production(adate)
    


if __name__=='__main__':
    arguments()
    main(ADATE)

