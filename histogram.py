# filename plot.py
#   plot dpc-covid19-ita-andamento-nazionale.csv data to graphs with lines
#   one graph is in italian language, the other one is in english

help = '''python plot.py datafile 
where datafile is:
    - "data"                        
    - "stato"                       
    - "ricoverati_con_sintomi"      
    - "terapia_intensiva"           
    - "totale_ospedalizzati"        
    - "isolamento_domiciliare"      
    - "totale_attualmente_positivi" 
    - "nuovi_attualmente_positivi"  
    - "dimessi_guariti"             
    - "deceduti"                    
    - "totale_casi"                 
    - "tamponi"                     
'''

#import csv
import os
import statistics as stats
import sys

#import numpy as np
#from enum import IntEnum
from datetime import datetime, date
from pathlib import Path

from matplotlib import pyplot as plt, dates as mdates

import pandas            as pd

import plot as p
import utils as u

#DIR_IMG  = './images'
#DIR_DATA = './data'
FN = 'dpc-covid19-ita-regioni.csv'
FNOUT = 'dpc-covid19-ita-regioni-shrinked.csv'
#TITLE_IT = 'covid-19, italia, andamento regionale dei casi positivi\nultimi {} giorni dal {}'
#TITLE_EN = 'covid-19, italy, regional trends of positive cases\nlast {} days since {}'
TITLE_IT = 'covid-19, italia, distribuzione regionale dei casi positivi'
TITLE_EN = 'covid-19, italy, regional trend of positive cases'
ITDT_FMT = '%d.%m.%Y'
ENDT_FMT = '%m.%d %Y'
NUM_DAYS = 1
REGIONS = {
    'Piemonte': 'Piemonte',
    "Valle d'Aosta": "V.d'Aosta",
    'Lombardia': 'Lombardia',
    'P.A. Bolzano': 'Bolzano',
    'P.A. Trento': 'Trento',
    'Bolzano': 'Bolzano',
    'Trento': 'Trento',
    'Veneto': 'Veneto',
    'Friuli Venezia Giulia': 'Friuli V.Giulia',
    'Friuli V. G. ': 'Friuli V.Giulia',
    'Liguria': 'Liguria',
    'Emilia Romagna': 'E.Romagna',
    'Toscana': 'Toscana',
    'Umbria': 'Umbria',
    'Marche': 'Marche',
    'Lazio': 'Lazio',
    'Abruzzo': 'Abruzzo',
    'Molise': 'Molise',
    'Campania': 'Campania',
    'Puglia': 'Puglia',
    'Basilicata': 'Basilicata',
    'Calabria': 'Calabria',
    'Sicilia': 'Sicilia',
    'Sardegna': 'Sardegna',
}
BZTN_ID = 4          #region identifier for trento and bolzano


def get_regions(df):
    #import pdb; pdb.set_trace()
    regions = df['codice_regione']
    regions = regions.drop_duplicates()
    regions = regions.sort_values()
    return list(regions)

    
def get_regions_name(df, l):
    names = []
    for code in l:
        name = df[df['codice_regione']==code].iloc[0]['denominazione_regione'][:]
        names.append(name)
    return names
    
    
def shape_data(df):
    '''
    convert data column from string to date
    '''
    # data from str to date
    df['data'] = df['data'].map(lambda x: datetime.strptime(x, u.DT_FMT).date())
    
    #    # change ID of Trento: here it is the same of Bolzano
    trento_id = df['codice_regione'].max() + 1
    df.loc[df['denominazione_regione'].str.contains('Trento'), 'codice_regione'] = trento_id
    
    # drop all columns that are not present in cols
    df_cols = list(df.columns)
    for col in df_cols:
        if not col in u.COLUMNS_RITALY['it'].keys():
            df.drop(col, axis=1, inplace=True)

    return df
    

#def shape_data_0(v):
#    '''from v as strs and all data to right values and only useful data
#    '''
#    v2 = str_to_values(v)
#    #print(f'len v2: {len(v2)}')
#    list_of_dates = u.get_date(v2)[-NUM_DAYS:]
#    #print(f'dates: {list_of_dates}')
#    tmp = []
#    for row in v2:
#        if row['data'] in list_of_dates:
#            tmp_row = dict()
#            tmp_row['data'] = row['data']
#            tmp_row['codice_regione'] = row['codice_regione']
#            tmp_row['denominazione_regione'] = row['denominazione_regione']
#            tmp_row['deceduti'] = row['deceduti']
#            tmp_row['dimessi_guariti'] = row['dimessi_guariti']
#            tmp_row['totale_attualmente_positivi'] = row['totale_attualmente_positivi']
#        else:
#            tmp_row = None
#        if tmp_row:
#            tmp.append(tmp_row)
#    return tmp

def get_dates(df):
    dates = df['data'].copy()
    dates = dates.drop_duplicates()
    dates = dates.sort_values()
    return list(dates)
    
def make_histogram(df, filename, lang='it'):
    '''write plot file in png format using data in df
    
       params
         - df             pandas dataframe
         - v              list of (shaped) dicts - [{data: val11, stato: val12, codice: val13, ...},
                                                    {data: val21, stato: val22, codice: val23, ...},
                                                    ... ]
         - filename       str - filename to use to plot, except its extension
         - lang           'it' or 'en
         
       return none
    '''
    
    list_of_dates = get_dates(df)[-NUM_DAYS:]
    
    regions = get_regions(df)                  # region IDs (names can change)
    
    width = 1/(NUM_DAYS+1)
    
    fig, ax = plt.subplots(1,1, figsize=(9,7))     # 900x700 px on my laptop
    fig.subplots_adjust(bottom=0.2)
    plt.grid(linestyle='--', axis='y')
    
    sdf1 = df[(df['data'].isin(list_of_dates))]       # out all dates < list_of_dates
    # here we get:        cod.regione ->      1    2    3 ...
    #          data ->  27/03/2020          100  200  300 ...    <- totale casi
    #                   ...                 ...           ...
    sdf11 = sdf1.pivot(index='data', columns='codice_regione', values='totale_casi')
    # x axis: region codes <-> names
    xvals = sdf11.columns.values.tolist()                  # list of region codes
    names = get_regions_name(df, xvals)                    # list of region names
    plt.xticks(range(len(xvals)), names, rotation=85)
    # dates of the bars
    dates = sdf11.index.values.tolist()
    # y axis: totla cases
    for ndx in range(len(dates)):
        date = dates[ndx]
        yvals = sdf11.loc[date].values.tolist()
        plt.bar([ x+(ndx*width) for x in range(len(xvals))], yvals , width=width, label=list_of_dates[ndx].strftime(u.D_FMT))
    
    if lang=='it':
        #plt.title(TITLE_IT.format(NUM_DAYS, list_of_dates[0].strftime(ITDT_FMT) ))                # set plot title
        plt.title(TITLE_IT)                # set plot title
        plt.xlabel("regioni")
        plt.ylabel("numero di casi positivi")
    else:
        #plt.title(TITLE_EN.format(NUM_DAYS, list_of_dates[0].strftime(ENDT_FMT) ))                # set plot title
        plt.title(TITLE_EN)                # set plot title
        plt.xlabel("regions")
        plt.ylabel("number of positive cases")
    
    plt.legend(loc="upper right")
    
    #plt.show()                                # show interactively 
    
    if lang=='it':
        plot_filename = os.path.splitext(filename)[0]+'.png'
    else:
        plot_filename = os.path.splitext(filename)[0]+'.en.png'
    plt.savefig(Path(u.DIR_IMG) / plot_filename, format='png') # show to file
    

def main(afile):
    #v = u.load_data(Path(u.DIR_DATA) / afile)
    #sd = shape_data(v)
    #save_data(sd, 'pippo.csv')
    df = pd.read_csv(Path(u.DIR_DATA) / afile)
    sd = shape_data(df)
    make_histogram(sd, afile, 'it')
    #make_histogram(sd, afile, 'en')


if __name__=='__main__':
    #print(len(sys.argv))
    if len(sys.argv) > 1:
        FN =  sys.argv[1][:]
    main(FN)
