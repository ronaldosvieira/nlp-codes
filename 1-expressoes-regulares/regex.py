#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

patterns = {
  'num': r'[0-9]+', 
  'data': (
    r'[0-3]?[0-9]' # dia
    r'(/|\s*de\s*)' # separador 1
    r'([0-3]?[0-9]|[jJ]aneiro|[fF]evereiro|[mM]arço|[aA]bril|[mM]aio|'
    r'[jJ]unho|[sS]etembro|[oO]utubro|[nN]ovembro|[dD]ezembro)' # mês
    r'((/|\s*de\s*)' # separador 2
    r'[0-9]{2,4})?'), # ano
  'endereco': r'[rR]ua \w+, \d+',
  'telefone': r'(\(\d{2}\))?\s*\d?\s*\d{4}\s*-?\s*\d{4}'
}

text = raw_input()

while text:
    text = re.sub(patterns['data'], '_DATA_', text)
    text = re.sub(patterns['telefone'], '_TELEFONE_', text)
    text = re.sub(patterns['endereco'], '_ENDERECO_', text)
    text = re.sub(patterns['num'], '_NUM_', text)
    
    print(text)
    
    text = raw_input()