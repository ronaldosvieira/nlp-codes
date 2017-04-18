#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys

patterns = {
  'num': r'[0-9]+', 
  'data': [
    r'[0-3]?[0-9]/[0-3]?[0-9](/[0-9]{2,4})?',
    (r'([0-2]?[0-9]\s*de\s*)?([jJ]aneiro|[fF]evereiro|[mM]arço|'
    r'[aA]bril|[mM]aio|[jJ]unho|[aA]gosto|[sS]etembro|[oO]utubro|'
    r'[nN]ovembro|[dD]ezembro)(\s*de\s*[0-9]{2,4})?')
  ],
  'endereco': r'[rR]ua \w+, \d+',
  'telefone': r'(\(\d{2}\))?\s*\d?\s*\d{4}\s*-?\s*\d{4}'
}

for line in sys.stdin:
  line = line.rstrip("\r\n")
  
  line = re.sub(patterns['data'][0], '_DATA_', line)
  line = re.sub(patterns['data'][1], '_DATA_', line)
  line = re.sub(patterns['telefone'], '_TELEFONE_', line)
  line = re.sub(patterns['endereco'], '_ENDERECO_', line)
  line = re.sub(patterns['num'], '_NUM_', line)
  
  print(line)