# filename table.py
#   transform csv data file to table 
#   one graph is in italian language, the other one is in english

help = '''python table.py datafile 
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

import csv
from datetime import datetime, date
from pathlib import Path
import sys

## Note: we won't change FIELDS. If we need to change p.FIELDS, THIS WOULD BE the correct way to do it
#from plot import FIELDS as FIELDS
import plot  as p
import utils as u

TAB_TITLE    = "Serie storiche dell'infezione covid-2019 per l'Italia; fonte: Ministero Sanita, tramite Protezione Civile"
TAB_EN_TITLE = "Time series of covid-2019 infection for Italy; source: Ministry of Health, by Civil Protection"


def shape_data(v, cut=[]):
    '''from v as strs and all data to right values and only useful data
    '''
    v2 = []
    for row in v:
        tmp_row = dict()
        for key,value in row.items():
            if key in cut:
                continue
            if key=='data':
                adate = row[key] if isinstance(row[key], date) else datetime.strptime(row[key], u.DT_FMT).date()
                tmp_row[key] = adate.strftime(u.D_FMT)
            else:
                tmp_row[key] = row[key][:] if isinstance(row[key], str) else '{}'.format(row[key])
        v2.append(tmp_row)
    return v2


def get_width(v, f, lang='it'):
    '''get width of colums of v
    
       params: 
         - v          list of dicts - [{field1: val11, field2: val12, ...},
                                       {field1: val12, field2: val22, ...},
                                       ... ]
         - f          dict - { field1: {ndx: n1, it: italian1, en: english1},
                               field2: {ndx: n2, it: italian2, en: english2},
                               ... }
         - lang       'it' or 'en'
         
       return a dict {field1: width1, field2: width2, ...}
    '''
    w = dict()
    fields = v[0].keys()
    #import pdb; pdb.set_trace()
    for col in fields:          # ranging on columns
        lens = []
        lens.append(len(f[col][lang]))        # length of field header
        for row in v:                                # what if row is empty? (it happened)
            lens.append(len(row[col]))
        w[col] = max(lens)
    return w
    
#def get_date(v, f):
# prendere l'ultima data dall'elenco date di v

    
def rst_table(v, fields, lang='it', title=''):
    '''build a restructuredtext table from csv file
    
       params
         - v          list of dicts - [{fld1: val11, fld2: val12, ...},
                                       {fld1: val21, fld2: val22, ...},
                                       ... ]
         - fields     dict - { field1: {ndx: n1, it: italian1, en: english1},
                               field2: {ndx: n2, it: italian2, en: english2},
                                      ... }
         - lang       'it' or 'en'
       
       return
         - the rst table    list of str, one str every row
    '''
    
    ## read values from csv file
    #with open(Path(u.DIR_DATA) / filename, 'r') as f:
    #    v = list(csv.DictReader(f, delimiter=','))
        
    w = get_width(v, fields, lang)
    fieldnames = list(w.keys())
    
    rs = '+' + '+'.join(['-' * w[key] for key in fieldnames]) + '+'   # this is the row separator: +-----+----+ ... +----+
    rs1 = '+' + '-' * (len(rs) - 2) + '+'                             # this is the 1st row sep:   +----- ...        ----+
    
    # this is general title and fieldnames to build header
    if title:
        t = '|' + title.center(len(rs)-2) + '|'
    else:
        t = None
    if lang=='it':
        field_headers = [ fields[key]['it'].center(w[key]) for key in fieldnames]
    else:
        field_headers = [ fields[key]['en'].center(w[key]) for key in fieldnames]
    header = '|' + '|'.join(field_headers) + '|'                     # this is header: | field1 | field2 | ... |
        
    rst = []
    if t:
        rst.append(rs1[:])         # +--------------------- ...
        rst.append(t[:])           # | wonder table         ...
    rst.append(rs[:])              # +------+--------+----- ...
    rst.append(header[:])          # | fld1 | fld2   | fld3 ...
    
    for row in v:
        rst.append(rs[:])
        fieldvalues = [ row[key].ljust(w[key]) for key in fieldnames]
        rst.append('|' + '|'.join(fieldvalues) +'|')
    rst.append(rs[:])
    return rst


def make_table(filename, f, lang='it', title=''):
    '''build a restructuredtext table from csv file, returning it as a string
    
       params
         - filename          str, the csv file with data
         - f                 dict - { field1: {ndx: n1, it: italian1, en: english1},
                                      field2: {ndx: n2, it: italian2, en: english2},
                                      ... }
         - lang             str, 'it' or something else meaning english
         
       return
         - the rst table    str, one single big string
    '''
    
    rst = rst_table(filename, f, lang, title)
    return '\n'.join(rst)


def main(filename):
    v = u.load_data(Path(u.DIR_DATA) / afile)
    sd = shape_data(v)

    rst_it = make_table(sd, p.FIELDS, 'it', TAB_TITLE)
    with open(filename+'.rst', 'w') as f: 
        f.write(rst_it)

    rst_en = make_table(sd, p.FIELDS, 'en', TAB_EN_TITLE)
    with open(filename+'.en.rst', 'w') as f: 
        f.write(rst_en)


if __name__=='__main__':
    if len(sys.argv) > 1:
        p.FN =  sys.argv[1][:]
    main(p.FN)
