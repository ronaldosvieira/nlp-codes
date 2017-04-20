#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import unicodedata

def tokenize(text):
    tokens = list()
    
    for pre_token in re.split(r"\s+", text):
        split_token = [i for i in re.split(r"([^\w\d]$)", pre_token) if len(i) > 0]
        
        tokens = tokens + split_token
    
    return tokens

def remove_accents(word):
    return "".join((c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn'))

def main():
    text = ''.join([re.sub(r"[(\r+)(\n+)(\t+)]", " ", line) for line in sys.stdin])
    text = remove_accents(text)
    
    print('\n'.join(tokenize(text)))
        
if __name__ == '__main__':
    main()