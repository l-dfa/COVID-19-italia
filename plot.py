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
import sys

from datetime import datetime, date
from pathlib import Path

from matplotlib import pyplot as plt, dates as mdates
import pandas   as pd

import utils as u

FN = 'dpc-covid19-ita-andamento-nazionale.csv'
RFN = 'dpc-covid19-ita-regioni.csv'
IMG_MOST_HITTED_RFN = 'dpc-covid19-ita-regioni_most_hitted.png'
IMG_MOST_HITTED_RFN = 'dpc-covid19-ita-regioni_most_hitted.png'
TITLE_IT = 'covid-19, italia'
TITLE_EN = 'covid-19, italy'
N_MOST_HITTED = 6

X11 = (
    'aqua',
    'aquamarine',
    'beige',
#    'black',
    'blue',
    'brown',
    'cyan',
    'darkblue',
    'darkgreen',
    'fuchsia',
    'gold',
    'green',
    'grey',
    'khaki',
    'lime',
    'magenta',
    'navy',
    'olive',
    'orangered',
    'purple',
    'red',
    'salmon',
    'silver',
    'violet',
#    'white',
    'yellow',
    'yellowgreen',
)

#COLORMAP = 'inferno_r'
COLORMAP = 'Set1'
    
def shape_data(df):
    '''
    convert data column from string to date
    '''
    # data from str to date
    df['data'] = df['data'].map(lambda x: datetime.strptime(x, u.DT_FMT).date())
    
    return df
    
def make_rplot(rdf, filename, **kwargs):
    '''
    line chart of regional trend
    
    params: 
      - rdf          pandas dataframe - see u.COLUMNS_RITALY
      - filename     str - filename of dataset, used to derive the plot filename
      - **kwargs     dict - of arguments
        - min          int - min index of countries to plot
        - max          int - max index of countries to plot
        - xlabel,      str - label of x axis
        - ylabel,      str - label of y axis
        - title,       str - title of picture
        - lang         'it' | 'en'
    
    return None
    
    side effect: store a file containing the draw
    
    note: see https://pythonconquerstheuniverse.wordpress.com/2012/02/15/mutable-default-arguments/
          about how manage mutable default arguments (list, dict, ...)
    '''
    
    params = {'min', 'max', 'xlabel', 'ylabel', 'title', 'lang'}
    keys = set(kwargs.keys())
    if not keys <= params:
        raise KeyError('make_rplot, unknown parameters: {}'.format(keys-params))
    for dkey in params - keys:
        if dkey == 'min': kwargs['min'] = -N_MOST_HITTED
        elif dkey == 'max': kwargs['max'] = None
        elif dkey == 'xlabel': kwargs['xlabel'] = ''
        elif dkey == 'ylabel': kwargs['ylabel'] = ''
        elif dkey == 'title': kwargs['title'] = ''
        elif dkey == 'lang': kwargs['lang'] = 'it'
        else: 
            raise KeyError('make_rplot, what is it happening? {} is awkward'.format(dkey))
    
    #import pdb; pdb.set_trace()
    bymax = rdf.groupby(by='codice_regione').agg(max).sort_values('totale_casi')
    nmh = bymax.iloc[kwargs['min']:kwargs['max']] if kwargs['max'] is not None else bymax.iloc[kwargs['min']:]
    regions = nmh['denominazione_regione']
    
    srdf1 = rdf[rdf['denominazione_regione'].isin(regions)]
    
    srdf11 = srdf1.pivot(index='data', columns='denominazione_regione', values='totale_casi')
    srdf11.sort_values(['data'], inplace=True)
    ax = srdf11.plot(
                    figsize=(9,7),
                    colormap=COLORMAP,
                    rot=80
                    )
    ax.grid(linestyle='--', axis='both')
    ax.set_title(kwargs['title'])
    ax.set_xlabel(kwargs['xlabel'])
    ax.set_ylabel(kwargs['ylabel'])
    fig = ax.get_figure()
    fig.subplots_adjust(bottom=0.2)
    
    if filename is None:
        plt.show()
    else:
        if kwargs['lang']=='it':
            plot_filename = os.path.splitext(filename)[0]+'.most_hitted.png'
        else:
            plot_filename = os.path.splitext(filename)[0]+'.most_hitted.en.png'
            
        ax.set_title(kwargs['title'])
        plt.savefig(Path(u.DIR_IMG) / plot_filename, format='png') # show to file
    plt.close()

    
def make_plot(df, filename, lang='it'):
    '''
    draw a line chart of national trend 
    
    params:
      - df          pandas dataframe - see u.COLUMNS_ITALY
      - filename    str - filename of dataset, used to derive the plot filename
      - lang        'it' or 'en'
    
    return None
    
    side effect: store a file containing the draw
    '''

    x        = df['data']
    totali   = df['totale_casi']
    positivi = df['totale_positivi']
    guariti  = df['dimessi_guariti']
    deceduti = df['deceduti']
    nuovi    = df['variazione_totale_positivi']
    
    fig = plt.figure(figsize=(9,7))
    #ax1 = fig.add_axes([0.1,0.3,0.8,0.6])  # left, bottom, width, height
    #ax2 = fig.add_axes([0.1,0.2,0.8,0.1], sharex=ax1)
    ax1 = fig.add_axes([0.1,0.35,0.8,0.6])  # left, bottom, width, height
    ax2 = fig.add_axes([0.1,0.20,0.8,0.15], sharex=ax1)
    
    ##plot figure with chosen language
    #plt.subplot(7,1,(1,6))
    ax1.grid(linestyle='--', axis='both')
    ax1.spines['right'].set_color(None)
    ax1.spines['top'].set_color(None)

    ax1.plot(x, totali,   'b', label=u.COLUMNS_ITALY[lang]['totale_casi'])             # plotting values
    ax1.plot(x, positivi, 'r', label=u.COLUMNS_ITALY[lang]['totale_positivi'])
    ax1.plot(x, guariti,  'g', label=u.COLUMNS_ITALY[lang]["dimessi_guariti"]) 
    ax1.plot(x, deceduti, 'k', label=u.COLUMNS_ITALY[lang]['deceduti'])
    #ax1.set_xticklabels([])                                # doesn't work
    #ax1.tick_params(axis='x', labelrotation=30)             # to hide under ax2
    ax1.tick_params(axis='x', labelrotation=90)             # to hide under ax2
    ax1.legend(loc="upper left")
    
    #plt.subplot(7,1,7)
    ax2.grid(linestyle='--', axis='both')
    ax2.spines['right'].set_color(None)
    ax2.plot(x, nuovi, 'r', label=u.COLUMNS_ITALY[lang]['variazione_totale_positivi'])
    ax2.legend(loc="upper left")
    ax2.tick_params(axis='x', labelrotation=80)
    #ax2.set_xticklabels(x, rotation=85, horizontalalignment='right')
    
    #plt.show()                                # show interactively 
    #sys.exit(0)

    if lang=='it':
        fig.suptitle(TITLE_IT)                # set plot title
        ax1.set_ylabel("numero di casi")
        ax2.set_ylabel("n.ro di casi")
        ax2.set_xlabel("data")
    else:
        fig.suptitle(TITLE_EN)                # set plot title
        ax1.set_ylabel("number of cases")
        ax2.set_ylabel("num. of cases")
        ax2.set_xlabel("date")
    
    if lang=='it':
        plot_filename = os.path.splitext(filename)[0]+'.png'
    else:
        plot_filename = os.path.splitext(filename)[0]+'.en.png'
        
    plt.savefig(Path(u.DIR_IMG) / plot_filename, format='png') # show to file
    return


def make_national(df, column, filename, **kwargs):
    '''
    line chart of time trend of national daily cases
    
    params: 
      - df          pandas dataframe - see u.COLUMNS_RITALY
      - filename     str - filename of dataset, used to derive the plot filename
      - min, max, xlabel, ylabel, title, lang
    
    return None
    
    side effect: store a file containing the draw
    
    note: see https://pythonconquerstheuniverse.wordpress.com/2012/02/15/mutable-default-arguments/
          about how manage mutable default arguments (list, dict, ...S)
    '''
    
    params = {'legend', 'xlabel', 'ylabel', 'title', 'lang'}
    keys = set(kwargs.keys())
    if not keys <= params:
        raise KeyError('make_national_daily, unknown parameters: {}'.format(keys-params))
    for dkey in params - keys:
        if   dkey == 'legend': kwargs['legend'] = False
        elif dkey == 'xlabel': kwargs['xlabel'] = ''
        elif dkey == 'ylabel': kwargs['ylabel'] = ''
        elif dkey == 'title':  kwargs['title']  = ''
        elif dkey == 'lang':   kwargs['lang']   = 'it'
        else: 
            raise KeyError('make_national_daily, what is it happening? {} is awkward'.format(dkey))
    
    #import pdb; pdb.set_trace()
    df.sort_values(['data'], inplace=True)
    ax = df.plot( x='data',
                  y=column,
                  legend=kwargs['legend'],
                  figsize=(9,7),
                  rot=80
                )
    ax.grid(linestyle='--', axis='both')
    ax.set_title(kwargs['title'])
    ax.set_xlabel(kwargs['xlabel'])
    ax.set_ylabel(kwargs['ylabel'])
    fig = ax.get_figure()
    fig.subplots_adjust(bottom=0.2)
    
    if filename is None:
        plt.show()
    else:
        if kwargs['lang']=='it':
            plot_filename = os.path.splitext(filename)[0]+'.nuovi_positivi.png'
        else:
            plot_filename = os.path.splitext(filename)[0]+'.nuovi_positivi.en.png'
            
        ax.set_title(kwargs['title'])
        plt.savefig(Path(u.DIR_IMG) / plot_filename, format='png') # show to file
    plt.close()

    


def main(afile):
    # national trend
    #df = pd.read_csv(Path(u.DIR_DATA) / afile)
    #df = shape_data(df)
    #make_plot(df, afile, 'it')
    #make_plot(df, afile, 'en')

    #regional trend
    #df = u.load_df(Path(u.DIR_DATA) / afile, pd.read_csv, u.COLUMNS_RITALY['it'], encoding='utf-8')
    #df = shape_data(df)
    #make_rplot(df, afile, xlabel='data', ylabel='numero totale di casi', title=f'Covid-19: andamento temporale per le {N_MOST_HITTED} regioni più colpite', lang = 'it' )
    #make_rplot(df, afile, xlabel='date', ylabel='total number of cases', title=f'Covid-19: temporal trend for the {N_MOST_HITTED} most hitted regions', lang = 'en' )

    df = u.load_df(Path(u.DIR_DATA) / afile, pd.read_csv, u.COLUMNS_ITALY['it'], encoding='utf-8')
    df = shape_data(df)
    make_national(df, 'nuovi_positivi', afile, xlabel='data', ylabel='numero giornaliero di nuovi casi', title=f'Covid-19: andamento temporale giornaliero di nuovi positivi (nazionale)', lang = 'it' )
    make_national(df, 'nuovi_positivi', afile, xlabel='date', ylabel='daily number of new cases', title=f'Covid-19: time trend of daily (national) new cases', lang = 'en' )

if __name__=='__main__':
    #print(len(sys.argv))
    if len(sys.argv) > 1:
        FN =  sys.argv[1][:]
    main(FN)
