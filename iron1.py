import os
import re
import sys
import glob
import argparse


if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog='iron.py', description='Extraxt info from Ironbeam text-file')
  parser.add_argument('folder',        help='Text input filename')
  args = parser.parse_args()
  print(args)

  files = glob.glob(f'{args.folder}/*.txt')

  out = {}
  for file in files:

    f = open(file, 'r')
    d = f.readlines()

    res = {}
    i = start = 0
    key = ''
    for l in d:
      match = re.search('<<<<<<<<<<(.*)>>>>>>>>>>', l)
      if not match is None:
        if key != '':
          res[key] = (start, i)
        start = i
        key = match.group(1).strip().replace(' ','_')
      i += 1

    for key in res.keys():
      d1 = d[res[key][0]:res[key][1]]
      if not key in out.keys():
        out[key] = d1
      else:
        out[key] += d1

  for key in out.keys():
    with open(f'{args.folder}/{key}.out', "w") as outfile:
      o = list(filter(lambda x: not x.isspace() and x!='\n', out[key]))
      outfile.write(''.join(o))

  print( [ (k,len(out[k])) for k in out.keys()] )
