#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import unicodedata

def sentence_tokenize(text):
    sentences = list()
    
    pre_tokens = re.split(r"([\.\;\?\!\:]+)", text)
    
    for p in range(0, len(pre_tokens) - 2, 2):
        sentences.append( pre_tokens[p] +  pre_tokens[p+1] )
    
    return sentences

def remove_accents(word):
    return "".join((c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn'))

def main():
    text = ''.join([re.sub(r"[(\r+)(\n+)(\t+)]", " ", line) for line in sys.stdin])
    text = remove_accents(text)
    
    print(' ->  ' + '\n -> '.join(sentence_tokenize(text)))
        
if __name__ == '__main__':
    main()