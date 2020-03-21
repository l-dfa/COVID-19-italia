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

import statistics as stats
import csv
import numpy as np
import os
#from enum import IntEnum
from datetime import datetime, date
from pathlib import Path
from matplotlib import pyplot as plt, dates as mdates
import sys
import plot as p
import utils as u

#DIR_IMG  = './images'
#DIR_DATA = './data'
FN = 'dpc-covid19-ita-regioni.csv'
FNOUT = 'dpc-covid19-ita-regioni-shrinked.csv'
TITLE_IT = 'covid-19, italia, andamento regionale dei casi positivi\nultimi {} giorni dal {}'
TITLE_EN = 'covid-19, italy, regional trends of positive cases\nlast {} days since {}'
#DT_FMT = '%Y-%m-%d %H:%M:%S'
#D_FMT = '%Y-%m-%d'
ITDT_FMT = '%d.%m.%Y'
ENDT_FMT = '%m.%d %Y'
NUM_DAYS = 4
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

FIELDS = {
    "data" :            {'ndx': 0, 'it': "data", 'en': "date",},                         # in shaped
    "stato" :           {'ndx': 1, 'it': "stato", 'en': "state",},
    "codice_regione" :  {'ndx': 2, 'it': "cod.regione", 'en': "region id.",},            # in shaped
    "denominazione_regione" :  {'ndx': 3, 'it': "nome regione", 'en': "region name",},   # in shaped
    "lat" :             {'ndx': 4, 'it': "lat",  'en': "lat",},
    "long" :            {'ndx': 5, 'it': "long", 'en': "long",},
    "ricoverati_con_sintomi" : {'ndx': 6, 'it': "ricoverati",      'en': "hospitalized",},
    "terapia_intensiva" :      {'ndx': 7, 'it': "terapia intens.", 'en': "intensive care",},
    "totale_ospedalizzati" :   {'ndx': 8, 'it': "totale ricov.",   'en': "overall hospit.",},
    "isolamento_domiciliare" : {'ndx': 9, 'it': "domiciliare",    'en': "at home",},
    "totale_attualmente_positivi" : {'ndx': 10, 'it': "positivi", 'en': "positives",},         # in shaped
    "nuovi_attualmente_positivi" :  {'ndx': 11, 'it': "variazione positivi", 'en': "change of positives",}, 
    "dimessi_guariti" : {'ndx': 12, 'it': "guariti",  'en': "healed",},                   # in shaped
    "deceduti" :        {'ndx': 13, 'it': "deceduti", 'en': "deceased",},                # in shaped
    "totale_casi" :     {'ndx': 14, 'it': "totali",   'en': "overall",},                   # in shaped
    "tamponi" :         {'ndx': 15, 'it': "tamponi",  'en': "swab",},
}



def str_to_values(v):
    '''
       Note. Using a list of dicts:
           [{data, stato, codice, ...},
            {data, stato, codice, ...},
            ...
            {data, stato, codice, ...},
            ]
    '''
    # change dicts values from strings to the correct values
    tmp = []
    for row in v:
        tmp_row = dict()
        for key, value in row.items():
            try:
                if key=='data':                        # date is 'aaaa/mm/gg hh:mm:ss'
                    tmp_row[key] = datetime.strptime(value, u.DT_FMT).date()
                elif key == 'stato':
                    tmp_row[key] = value[:]
                elif key == 'denominazione_regione':   # change with our names
                    tmp_row[key] = REGIONS[value][:]
                elif key in ('lat', 'long', ):
                    tmp_row[key] = float(value)
                else:                                  # other elements: try to convert to int, if fails, set to None
                    tmp_row[key] = int(value)
            except ValueError:
                tmp_row[key] = None
                print('verror: {}, {}, {}'.format(row['data'],row['denominazione_regione'],key ))
            except KeyError:
                print('kerror: {}, {}'.format(row['data'],row['denominazione_regione'] ))
        tmp.append(tmp_row)
    # change ID of Trento: here it is the same of Bolzano
    region_ids = get_regions(tmp)
    trento_id = max(region_ids) + 1
    tmp2 = []
    for row in tmp:
        tmp_row = dict(row)
        if row['denominazione_regione']=='Trento':
            tmp_row['codice_regione'] = trento_id
        tmp2.append(tmp_row)
    return tmp2
    
def get_regions(v):
    l = list( set( [row['codice_regione'] for row in v] ) )
    return sorted(l)


def save_data(v, filename=FNOUT):
    # make a copy of v to delete 'codice_regione' without altering v
    v2 = []
    for row in v:
        v2.append(dict(row))
    for row in v2:
        del row['codice_regione']
    return u.save_data(v2, Path(u.DIR_DATA) / filename)


def get_regions_name(v, l):
    names = []
    for code in l:
        for row in v:
            if row['codice_regione']==code:
                names.append(row['denominazione_regione'][:])
                break
    return names
    
    
def shape_data(v):
    '''from v as strs and all data to right values and only useful data
    '''
    v2 = str_to_values(v)
    #print(f'len v2: {len(v2)}')
    list_of_dates = u.get_date(v2)[-NUM_DAYS:]
    #print(f'dates: {list_of_dates}')
    tmp = []
    for row in v2:
        if row['data'] in list_of_dates:
            tmp_row = dict()
            tmp_row['data'] = row['data']
            tmp_row['codice_regione'] = row['codice_regione']
            tmp_row['denominazione_regione'] = row['denominazione_regione']
            tmp_row['deceduti'] = row['deceduti']
            tmp_row['dimessi_guariti'] = row['dimessi_guariti']
            tmp_row['totale_attualmente_positivi'] = row['totale_attualmente_positivi']
        else:
            tmp_row = None
        if tmp_row:
            tmp.append(tmp_row)
    return tmp
    
    
def make_histogram(v, filename, lang='it'):
    '''write plot file in png format using data in v
    
       params
         - v              list of (shaped) dicts - [{data: val11, stato: val12, codice: val13, ...},
                                                    {data: val21, stato: val22, codice: val23, ...},
                                                    ... ]
         - filename       str - filename to use to plot, except its extension
         - lang           'it' or 'en
         
       return none
    '''
    #language = 1 if lang=='it' else 2
    
    list_of_dates = u.get_date(v)[-NUM_DAYS:]
    regions = get_regions(v)                  # region IDs (names can change)
    
    width = 1/(NUM_DAYS+1)
    
    fig, ax = plt.subplots(1,1, figsize=(9,7))     # 900x700 px on my laptop
    fig.subplots_adjust(bottom=0.2)
    plt.grid(linestyle='--', axis='y')
    
    # we wanna do a list of lists as follows:
    # [[(id_regione1, dato), (id_regione2, dato), ...]     # date1
    #  [(id_regione1, dato), (id_regione2, dato), ...]     # date2
    #  ...  ]                                              # ...
    
    list_of_values = []
    for adate in list_of_dates:
        values = [(record['codice_regione'], record['totale_attualmente_positivi'],) for record in v if record['data']==adate]
        list_of_values.append(values)
    xvals = [n[0] for n in list_of_values[0]]   # these are:     [id_regione1, id_regione2, ...] from the 1st row; they must be all equals
    names = get_regions_name(v, xvals)          # and these are: [name_regione1, name_regione2, ...]
    
    plt.xticks(range(len(xvals)), names, rotation=85)
    for ndx in range(len(list_of_values)):
        yvals = [n[1] for n in list_of_values[ndx]]
        plt.bar([ x+(ndx*width) for x in range(len(xvals))], yvals , width=width, label=list_of_dates[ndx].strftime(u.D_FMT))
        
    if lang=='it':
        plt.title(TITLE_IT.format(NUM_DAYS, list_of_dates[0].strftime(ITDT_FMT) ))                # set plot title
        plt.xlabel("regioni")
        plt.ylabel("numero di casi positivi")
    else:
        plt.title(TITLE_EN.format(NUM_DAYS, list_of_dates[0].strftime(ENDT_FMT) ))                # set plot title
        plt.xlabel("regions")
        plt.ylabel("number of positive cases")
    
    plt.legend(loc="upper left")
    
    #plt.show()                                # show interactively 
    
    if lang=='it':
        plot_filename = os.path.splitext(filename)[0]+'.png'
    else:
        plot_filename = os.path.splitext(filename)[0]+'.en.png'
    plt.savefig(Path(u.DIR_IMG) / plot_filename, format='png') # show to file
    

def main(afile):
    v = u.load_data(Path(u.DIR_DATA) / afile)
    sd = shape_data(v)
    save_data(sd, 'pippo.csv')
    make_histogram(sd, afile, 'it')
    make_histogram(sd, afile, 'en')


if __name__=='__main__':
    #print(len(sys.argv))
    if len(sys.argv) > 1:
        FN =  sys.argv[1][:]
    main(FN)
