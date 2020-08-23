installed: matplotlib, pandas, xlrd (excel reader)

to read excel files (font: https://grokonez.com/python/ways-to-convert-an-excel-file-to-csv-file-in-python-3)::

  import pandas as pd
   
  df = pd.read_excel('grokonez.xlsx')  # parameter (sheetname='sheet_name') is optional
  df.to_csv('grokonez.csv', index=False)  # index=True to write row index
  
to list installed packets::

  pip freeze >requirements.txt
  
to reinstall required packets::

  pip install -r requirements.txt
  
pandas tutorial for beginners: https://www.learndatasci.com/tutorials/python-pandas-tutorial-complete-introduction-for-beginners/

remark: converting file COVID-19-geographic-disbtribution-worldwide.xlsx to csv 
format generate a wrong denomination for Curaçao. The ç character is bad coded.
So it is necessary edit this country name(s).