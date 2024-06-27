import re
import sys
import pandas as pd

import argparse

DATE = '2024-12-31'

def get_cols(h_):
  cols = [0]
  i = h_.find(' ')
  while i != -1:
    cols.append(i+1)
    i = h_.find(' ' ,i+2)
  cols.append(len(h_))
  return cols

def split_rows(d_, cols_):
  rows=[]
  i = 0
  at_end = True
  while i<len(d_):
    l = d_[i]
    if not re.search('<<<<<<<<<<(.*)>>>>>>>>>>', l) is None:
      i += 1
      continue     
    if not re.search('\*\*\*\*\*\*\*\*\*', l) is None:
      i += 1
      continue
    if not re.search('=======================', l) is None:
      at_end = True
      i += 1
      continue
    if not re.search('TRANSACTION', l) is None:
      at_end = False
      i += 1
      continue
    if not at_end:
      row = []
      start = cols_[0]
      for end in cols_[1:]:
        row.append(l[start:end].strip())
        start = end
      rows.append(row)
    i += 1
  return rows
  

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog='iron2.py', description='Extraxt purchase and sales info from Ironbeam out-file (created by iron1.py)')
  parser.add_argument('infile',        help='Text input filename')
  parser.add_argument('filetype',      help='Type of file', choices=['conf','pur'], default='pur')
  parser.add_argument('--colnames',    help='Columns names for CSV file',
                      default='BUY,SELL,BOX CODE,EXCH,TRANSACTION/PRODUCT DESCRIPTION,EX DATE,C,STRIKE PRICE,TRADE PRICE,AMOUNT,DATE')
  args = parser.parse_args()
  print(args)

  f = open(args.infile)
  d = f.readlines()

  if args.filetype=='pur':
    # use row 3 to figure out where columns start
    cols = get_cols(d[3])

    # split lines according to columns
    rows = split_rows(d[2:], cols)
    df = pd.DataFrame(rows)

    df = df[(df.iloc[:,0]!='--------') & (df.iloc[:,0].str.strip()!='BUY')]
    df = df[df.iloc[:,2].str.strip()!='BOX']
    df = df[df.iloc[:,0].str[-1]!='*']

    df.columns = args.colnames.split(',')
    df['Date'] = pd.to_datetime(df['DATE'], format='%d%b%y')
    df['Shares'] = df.BUY.replace('',0).astype(int) - df.SELL.replace('',0).astype(int)
    df['type'] = 'Long'
    df.loc[df.Shares<0,'type'] = 'Short'

  if args.filetype=='conf':
    # skip header with address etc.
    i = 0
    while re.search('TRANSACTION/PRODUCT DESCRIPTION', d[i]) is None:
      i += 1

    # use row i to figure out where columns start
    cols = get_cols(d[i+1])

    # split lines according to columns
    rows = split_rows(d[i:], cols)
    df = pd.DataFrame(rows)

    df = df[(df.iloc[:,0]!='--------') & (df.iloc[:,0].str.strip()!='BUY')]
    df = df[df.iloc[:,2].str.strip()!='BOX']
    df = df[df.iloc[:,0].str[-1]!='*']
    df.columns = args.colnames.split(',')

    df['Date'] = DATE
    df['type'] = 'Fee'
    df.loc[df['TRADE PRICE'] != '','type'] = 'Trade'
    df.to_csv(f'{args.infile.removesuffix(".out")}_all.csv', index=False)
    df = df.loc[df.type!='Trade']
    
  df.to_csv(f'{args.infile.removesuffix(".out")}.csv', index=False)

