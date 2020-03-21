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

import utils as u

#DIR_IMG  = './images'
#DIR_DATA = './data'
FN = 'dpc-covid19-ita-andamento-nazionale.csv'
TITLE_IT = 'covid-19, italia'
TITLE_EN = 'covid-19, italy'
DT_FMT = '%Y-%m-%d %H:%M:%S'

FIELDS = {
    "data" :                   {'ndx': 0,  'it': "data",            'en': "date",},
    "stato" :                  {'ndx': 1,  'it': "stato",           'en': "state",},
    "ricoverati_con_sintomi" : {'ndx': 2,  'it': "ricoverati",      'en': "hospitalized",},
    "terapia_intensiva" :      {'ndx': 3,  'it': "terapia intens.", 'en': "intensive care",},
    "totale_ospedalizzati" :   {'ndx': 4,  'it': "totale ricov.",   'en': "overall hospit.",},
    "isolamento_domiciliare" : {'ndx': 5,  'it': "domiciliare",     'en': "at home",},
    "totale_attualmente_positivi" : {'ndx': 6, 'it': "positivi",       'en': "ill",},
    "nuovi_attualmente_positivi" :  {'ndx': 7, 'it': "nuovi positivi", 'en': "new positives",}, 
    "dimessi_guariti" :        {'ndx': 8,  'it': "guariti",         'en': "healed",},
    "deceduti" :               {'ndx': 9,  'it': "deceduti",        'en': "deceased",},
    "totale_casi" :            {'ndx': 10, 'it': "totali",          'en': "overall",},
    "tamponi" :                {'ndx': 11, 'it': "tamponi",         'en': "swab",},
}

#def str_to_values(v):
#    v = v[1:]                                # no header(s) and tail
#    tmp = []
#    for row in v:
#        first = True
#        tmp_row = []
#        for e in row:
#            if first:                  # 1st element in row is date 'aaaa/mm/gg hh:mm:ss'
#                first = False
#                tmp_row.append(datetime.strptime(e, DT_FMT).date())
#            else:                      # other elements: try to convert to int, if fails, skip
#                try:
#                    tmp_row.append(int(e))
#                except ValueError:
#                    tmp_row.append(None)
#            tmp.append(tmp_row)
#    return tmp
    
def str_to_values(v):
    tmp = []
    for row in v:
        tmp_row = dict()
        for key, value in row.items():
            try:
                if key=='data':                  # 1st element in row is date 'aaaa/mm/gg hh:mm:ss'
                    tmp_row[key] = datetime.strptime(value, DT_FMT).date()
                else:                      # other elements: try to convert to int, if fails, skip
                    tmp_row[key] = int(value)
            except ValueError:
                tmp_row[key] = None
        tmp.append(tmp_row)
    return tmp
    
    
def shape_data(v):
    '''from v as strs and all data to right values and only useful data
    '''
    return str_to_values(v)
    
def make_plot(v, filename, lang='it'):
    ##language = 1 if lang=='it' else 2
    ## read values from csv file
    #with open(Path(u.DIR_DATA) / filename, 'r') as f:
    #    v = list(csv.reader(f, delimiter=','))
    #    
    ##from string to values and extrapolate series to show
    #v = str_to_values(v)
    
    x        = [v[r]['data']            for r in range(len(v))]
    totali   = [v[r]['totale_casi']     for r in range(len(v))]
    positivi = [v[r]['totale_attualmente_positivi'] for r in range(len(v))]
    guariti  = [v[r]['dimessi_guariti'] for r in range(len(v))]
    deceduti = [v[r]['deceduti']        for r in range(len(v))]
    #print(len(v))
    #print(len(guariti))
    #print(guariti)
    #sys.exit(0)
    
    #plot figure with italian language
    fig, ax = plt.subplots(1,1, figsize=(9,7))    # 900x700 px on my laptop
    fig.autofmt_xdate()                           # manage date format
    plt.plot(x, totali,   'b', label=FIELDS['totale_casi'][lang])             # plotting values
    plt.plot(x, positivi, 'r', label=FIELDS['totale_attualmente_positivi'][lang])
    plt.plot(x, guariti,  'g', label=FIELDS["dimessi_guariti"][lang]) 
    plt.plot(x, deceduti, 'k', label=FIELDS['deceduti'][lang])
    if lang=='it':
        plt.title(TITLE_IT)                # set plot title
        plt.xlabel("data")
        plt.ylabel("numero di casi")
    else:
        plt.title(TITLE_EN)                # set plot title
        plt.xlabel("date")
        plt.ylabel("number of cases")

    plt.legend(loc="upper left")
    plt.grid(True)
    #plt.show()                                # show interactively 
    if lang=='it':
        plot_filename = os.path.splitext(filename)[0]+'.png'
    else:
        plot_filename = os.path.splitext(filename)[0]+'.en.png'
        
    plt.savefig(Path(u.DIR_IMG) / plot_filename, format='png') # show to file
    

def main(afile):
    v = u.load_data(Path(u.DIR_DATA) / afile)
    sd = shape_data(v)
    make_plot(sd, afile, 'it')
    make_plot(sd, afile, 'en')


if __name__=='__main__':
    #print(len(sys.argv))
    if len(sys.argv) > 1:
        FN =  sys.argv[1][:]
    main(FN)
