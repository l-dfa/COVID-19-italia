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
import numpy             as np
import pandas            as pd
#import paramiko

import utils             as u

# START section: BEFORE to use these variables, INSERT DATE
TITLE10 = 'Covid-19: temporal trend of number of total cases from {};\n10 countries with the highest total of cases'
TITLE09 = 'Covid-19: temporal trend of number of total cases from {};\nfrom the 3rd to the 10th countries with the highest total of cases'
TITLEEU = 'Covid-19: temporal trend from {};\n10 European Union countries with the highest total of cases'
# END   section: BEFORE to use these variables, INSERT DATE

# from 27 march 2020 this is the new url, without date; and data are in csv format
SOURCE = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
FNAME  = 'covid19-worldwide-{}.csv'
FEUNAME  = 'covid19-worldwide_EU.csv'
FSNAME  = 'covid19-worldwide-{}_summary.csv'
# END   section: BEFORE to use these variables, INSERT DATE

FN_IT_TEMPLATE  = '210_coronavirus_mondo.rst'
FN_EN_TEMPLATE  = '211_coronavirus_mondo.en.rst'
ADATE = date.today().strftime(u.D_FMT)

DOWNLOAD   = True          # if true get data from Internet
PRODUCTION = True          # if true copy data to ldfa filesystem and production server

# European Union: 27 countries
EU = (
    "Austria",
    "Belgium",  
    "Bulgaria",  
    "Croatia",  
    "Cyprus",  
    "Czechia",  
    "Denmark",  
    "Estonia",  
    "Finland",  
    "France",  
    "Germany",  
    "Greece", 
    "Hungary", 
    "Ireland", 
    "Italy", 
    "Latvia", 
    "Lithuania", 
    "Luxembourg", 
    "Malta", 
    "Netherlands", 
    "Poland", 
    "Portugal", 
    "Romania", 
    "Slovakia", 
    "Slovenia", 
    "Spain", 
    "Sweden", 
)

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

    
def modify_by_area(df, tags=None, area=None):
    '''
    aggregation by geographical area
    
    params:
      - df           pandas dataframe
      - tag          str - name of area
      - area         lst of str - list of nations making the area
      
    return a dataframe of the area
    
    side effects:
      - calculate area population
      - SUBSTITUTE INPLACE of df area's countries with area_tag and population 
    '''
    
    if area is None: area = EU         # rem: this is ("Austria", "Belgium", "Bulgaria", ... )
    if tags is None: tags = {'country': 'European Union',
                             'geoid': 'EU',
                             'countryterritoryCode': 'EU'
                            }
    
    country = tags['country']          # only to spare some keystokes
    
    # calculating area population
    df_eu = df[df['country'].isin(area)]
    population = df_eu[['country', 'population']].drop_duplicates().sum()['population']
    
    # substituting single area countries with area name
    df.loc[df['country'].isin(area), 'country'] = country
    df.loc[df['country']==country, 'geoid'] = tags['geoid']
    if 'countryterritoryCode' in df.columns:
        df.loc[df['country']==country, 'countryterritoryCode'] = tags['countryterritoryCode']
    df.loc[df['country']==country, 'population'] = population

    # we need aggregate day by day over all countries of the area
    dates = df['date'].drop_duplicates()
    #     iterating over dates to sum cases and death: when done, every day, drop duplicate
    for adate in dates:
        df_area_on_day = df[(df['date']==adate) & (df['country']==country)]
        area_cases_on_day = df_area_on_day['cases'].sum()
        area_death_on_day = df_area_on_day['death'].sum()
        df.loc[((df['date']==adate) & (df['country']==country)), 'cases'] = area_cases_on_day
        df.loc[((df['date']==adate) & (df['country']==country)), 'death'] = area_death_on_day
        df.drop_duplicates(inplace=True)
    
    return df_eu    


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
    
    # sorting countries by total cases
    countries.sort_values(['total_cases'], inplace=True, ascending=False)
    return list(countries['country'])
    
def world_get_sum_on_last_day(df, countries=None):
    '''
    create a new dataframe with total cases and some other data
    
    params: 
      - df             pandas dataframe - input df
      - countries      list of str - names of requested countries; if None
                       is going to list all countries in df 
    
    return a new df with  columns:
      - 'date',         date
      - 'day',          int
      - 'month',        int
      - 'year',         int
      - 'cases',        int
      - 'death',        int
      - 'death/cases',  float
      - 'cases/population',  float
      - 'death/populaton',   float
      - 'country',      str
      - 'geoid'         str
    '''
    
    if countries is None:
        countries = df['country'].drop_duplicates()   # get a copy
        
    l = []           # will be: [[date, ... sum, country ...], [date, ... sum, country ...], ...]

    for country in countries:
        country_df = df.loc[df['country']==country].copy()
        the_cases  = country_df['cases'].sum()
        the_deaths = country_df['death'].sum()
        the_date  = country_df['date'].max()
        the_day   = the_date.day
        the_month = the_date.month
        the_year  = the_date.year
        geoid = country_df['geoid'].max()
        population = country_df['population'].max()
        if the_cases == 0:
            deathly = None
        else:
            deathly = the_deaths / the_cases
            
        if population:
            extension = the_cases / population
            deathly_on_population = the_deaths / population
        else:
            extension = None
            deathly_on_population = None
        
        l.append((the_date,
                  the_day, 
                  the_month, 
                  the_year, 
                  the_cases, 
                  the_deaths, 
                  deathly, 
                  country[:], 
                  geoid,
                  population,
                  extension,
                  deathly_on_population,
                  ))
        
    df2 = pd.DataFrame(l, columns=['date',
                                   'day', 
                                   'month', 
                                   'year', 
                                   'cases', 
                                   'death', 
                                   'death/cases', 
                                   'country', 
                                   'geoid',
                                   'population',
                                   'cases/population',
                                   'death/population',
                                   ])
    df2 = df2.sort_values('cases', ascending=False)
    return df2    
    
    
def make_spagetti(df, adate, afile, title=None, ss=0, se=10):
    '''
    plot one lines graph of n most hitted nations
    
    params: 
      - df            pandas dataframe - df contains day by day cases of every nation
                        with date as index and a nation every column
      - adate         date - (after cumsum) cut dates previous this one
      - afile         Path or str - file to save png
      - title         str - title of graph
      - ss            int - slice start
      - se            int - slice end
    
    return always 0
    
    side effects: plot one graph and save as png file
    '''
    
    if title is None:
        title = TITLE10.format(adate.strftime(u.D_FMT))
        
    # get 10 most hitted countries
    df2 = world_get_sum_on_last_day(df) # this is sorted by cases
    countries = df2['country'][ss:se]        # 10 most hitted nations
    
    # these are 10 colors to use
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
    
    # from df          date  ...  cases  ...                   country  id
    #       1060 2020-03-18  ...     33  ...                     China  CN
    #       1061 2020-03-17  ...    110  ...                     China  CN
    #       1062 2020-03-16  ...     25  ...                     China  CN
    #       ...         ...  ...    ...  ...                       ...  ..
    #       5441 2020-01-01  ...      0  ...  United_States_of_America  US
    #       5442 2019-12-31  ...      0  ...  United_States_of_America  US
    #
    # to sdfx   country     China  France  Germany  Iran  ...
    #           date                                      ...
    #           2019-12-31     27       0        0     0  ...
    #           ...
    #           2020-03-17    110    1210     1174  1053  ...
    #           2020-03-18     33    1097     1144  1178  ...
    # 
    # hereafter prepare data to plot top 10 countries
    
    sdf1 = df[(df['country'].isin(countries))]
    
    ## WARNING: next instruction is ok because dates are the same for these nations
    ##    BUT some countries have less dates then others; IF one of this nations 
    ##    enters in the top ten this instruction will raise exception
    #sdf11 = sdf1.pivot(index='date', columns='country', values='cases')
    #sdf11.sort_values(['date'], inplace=True)
    
    # this is very slow but manage missing days
    sdf11 = pivot_by_iteration(sdf1)
    
    #import pdb; pdb.set_trace()
    
    sdf11 = sdf11.cumsum()
    sdf11 = sdf11.loc[adate:]                   # 1st graph: out dates less then adate
    
    # plot and draw to file
    ax = sdf11.plot(title=title,
                    figsize=(9,7),
                    color=colors
                    )
    ax.grid(linestyle='--', axis='both')
    ax.set_ylabel('number of total cases')
    plt.savefig(afile, format='png') # show to file
    plt.close()
    #plt.show()
    
    # do we plot EU as a federation?
    return 0
    
    
def pivot_by_iteration(df):
    '''
    pivot a dataframe iterating over columns and dates
    
    params df        pandas dataframe
    
    return sdf       pandas dataframe
    
    remark.
      given a df as   date ... cases death country ... with:
        - date       a date
        - cases      the total cases on the day (i.e, 
                       - if march 01 2020 cases is 100 @ Italy and we have 10 new cases in Italy that day,
                       -  then: march 02 2020 cases value is 110 @ Italy)
        - death      the total number of deceased on the day (same consideration as above) 
        - country    a country
      example:   date ...     cases death country
                 2020-03-01   100   10    country1
                 2020-03-01   80    8     country2
                 ...
                 2020-03-01   101   11    countryN
      this function builds a dataframe as
                         country1 country2 ... countryN
            date
            2020-03-01   100      80           101
      where values in countryI are the cases in that country
      
      Warning: this function is pretty slow because iterate over rows
    '''
    
    # building an empty df with dates as index
    dates = df['date'].drop_duplicates().sort_values()
    sdf = pd.DataFrame(dates, columns=['date'])                  # df with dates
    countries = df['country'].drop_duplicates().tolist()
    sdf = sdf.reindex(sdf.columns.tolist() + countries, axis=1)   # add a column every country
    sdf.set_index('date', inplace=True)                           # dates to index
    
    # iterating over countries
    for country in countries:
        acountry = df[df['country']==country]
        # iterating over dates in a country
        for adate in acountry['date']:
            try:
                # what a mess to extract a value!
                # §§ CHECK §§
                sdf.loc[adate, country] = acountry[acountry['date']==adate]['cases'].values.tolist()[0]
            except:
                sdf.loc[adate, country] = np.nan
    
    #import pdb; pdb.set_trace()
    
  
    return sdf

    
def make_article(template, adate, df, df_world):
    '''
    istantiate an article merging a template with actual data
    
    params: 
      - template              str or Path - to a filename containing the template to use
      - adate                 date - to use as update date
      - df                    pandas dataframe - to use as source of data
                                  with EU countries bundled
      - df_world              pandas dataframe - as df, with EU countries unbundled
      
    return article            str - the composed article
    
    side effects: save article as file
    '''
    #get article template
    with open(template, 'r') as f:
        template_from_file = f.read()

    # remember current date
    dt = datetime.now()
    
    # get last day situation of 20 hittest nations
    if u.ENABLE_DEBUG:
        breakpoint()
    columns = ['date', 'cases', 'death', 'death/cases', 'cases/population', 'death/population', 'country' ]
    
    df2 = world_get_sum_on_last_day(df)[:20]
    data_table = df2.to_csv(columns=columns, index=False, float_format='%.5f')
    lines = data_table.split('\n')
    lines = ['  '+line for line in lines]
    data_table = '\n'.join(lines)
    data_table = data_table.replace('_', ' ')
    
    df2_world = world_get_sum_on_last_day(df_world)[:20]
    data_table_eu = df2_world.to_csv(columns=columns,index=False, float_format = '%.5f')
    lines2 = data_table_eu.split('\n')
    lines2 = ['  '+line for line in lines2]
    data_table_eu = '\n'.join(lines2)
    data_table_eu = data_table_eu.replace('_', ' ')

    # prepare variable contents
    d = dict()
    d['MODIFIED'] = dt.strftime(u.DT_FMT2)
    d['UPDATED']  = adate
    d['DATA_TABLE']  = data_table
    d['DATA_TABLE_EU']  = data_table_eu
    
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
    files = (fname, 
             FEUNAME, 
             FSNAME.format(adate),
            )
    for afile in files:
        copyfile(Path(u.DIR_DATA) / afile, u.DIR_LDFA['data_world'] / afile)
    
    # world images to ldfa directory
    files = (os.path.splitext(fname)[0]+'_1-10.png', 
             os.path.splitext(fname)[0]+'_3-10.png',
             os.path.splitext(fname)[0]+'_eu_1-10.png',
            )
    for afile in files:
        copyfile(Path(u.DIR_WIMG) / afile, u.DIR_LDFA['images_world'] / afile)
    return
    

def to_production(adate):
    '''
    copy files from the project filesystem to production server
    
    params: adate          date - the update date
    
    return None
    '''
    
    fname = FNAME.format(adate)                   # covid19-worldwide-{}.csv   with adate
    
    # list of data files
    data_files = (fname[:],
                  FEUNAME, 
                  FSNAME.format(adate),
                 )
    
    image_files = (os.path.splitext(fname)[0]+'_1-10.png', 
                   os.path.splitext(fname)[0]+'_3-10.png',
                   os.path.splitext(fname)[0]+'_eu_1-10.png',
                  )
    
    u.to_production(u.DIR_DATA, u.DIR_PRODUCTION['data_world'], u.DIR_WIMG, u.DIR_PRODUCTION['images_world'], data_files, image_files)
    
    return


def main(adate):
    if u.ENABLE_DEBUG:
        breakpoint(header=f'world.py, main({adate}), break before download data')
    # get data
    if DOWNLOAD:
        df = get_data(adate)
        if type(df) == type(None):        # we cannot do: df == None because if df is dataframe it raises ValueError
            print('data from Internet not updated. run interrupted')
            sys.exit(1)
    else:
        df = u.load_df(u.DIR_DATA+'/'+FNAME.format(adate), pd.read_csv, u.COLUMNS_WORLD['en'], encoding='cp1250')
    df = world_shape(df)
    
    df_world = df.copy()
    
    df_eu = modify_by_area(df)
    # make two graphs:
    #    10 most hitted countries
    make_spagetti(df,
                  datetime.strptime('2020-01-14', u.D_FMT).date(),
                  Path(u.DIR_WIMG) / (os.path.splitext(FNAME.format(adate))[0]+'_1-10.png'),
                  title=TITLE10.format('2020-01-14'),
                  ss=0, se=10
                 )

    #    from 3rd to 10th of the 10 most hitted countries
    make_spagetti(df,
                  datetime.strptime('2020-02-20', u.D_FMT).date(),
                  Path(u.DIR_WIMG) / (os.path.splitext(FNAME.format(adate))[0]+'_3-10.png'),
                  title=TITLE09.format('2020-02-20'),
                  ss=2, se=10
                 )
                 
    #    from 1st to 10th of the 10 most hitted EU countries
    make_spagetti(df_eu,
                  datetime.strptime('2020-02-20', u.D_FMT).date(),
                  Path(u.DIR_WIMG) / (os.path.splitext(FNAME.format(adate))[0]+'_eu_1-10.png'),
                  title=TITLEEU.format('2020-02-20'),
                  ss=0, se=10
                 )
    
    # make articles
    make_article(u.DIR_TEMPLATE+'/'+FN_IT_TEMPLATE, adate, df, df_world)
    make_article(u.DIR_TEMPLATE+'/'+FN_EN_TEMPLATE, adate, df, df_world)
    
    # make summary about all world and save it to disk
    df2 = world_get_sum_on_last_day(df_world)
    columns = ['date', 'cases', 'death', 'death/cases', 'cases/population', 'death/population', 'country' ]
    df2.to_csv(Path(u.DIR_DATA) / FSNAME.format(adate),
                columns=columns,
                index=False,
                float_format = '%.6f')

    df.to_csv(Path(u.DIR_DATA) / FEUNAME,
              index=False,
             )
    
    # copy results to ldfa filesystem and to production
    if u.ENABLE_LDFA:
        to_ldfa(adate)
    if u.ENABLE_PRODUCTION:
        to_production(adate)


if __name__=='__main__':
    arguments()
    main(ADATE)

