#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def plural_reduction(word):
    plural = {'ns': ('m', 1, [])}
    
    matches = [suffix for suffix in plural.keys() 
        if word[-len(suffix):] == suffix and word not in plural[suffix][2]]
    
    if matches:
        suffix = matches[0]
        
        word = word[:-len(suffix)] + plural[suffix][0]
    
    return word

def feminine_reduction(word):
    return word
def augmentative_reduction(word):
    return word
def adverb_reduction(word):
    return word
def noun_reduction(word):
    return word

def suffix_removed(word):
    return word

def verb_reduction(word):
    return word

def remove_vowel(word):
    return word

def remove_accents(word):
    return word

def init():
    for line in sys.stdin:
        line = line.rstrip("\r\n")
        words = line.split(" ")
        stemmed_words = []
        
        for i in range(0, len(words)):
            word = words[i]
          
            if word[-1] == 's':
                word = plural_reduction(word)
                  
            if word[-1] == 'a':
                word = feminine_reduction(word)
                  
            word = augmentative_reduction(word)
            word = adverb_reduction(word)
            word = noun_reduction(word)
            
            if not suffix_removed(word):
                word = verb_reduction(word)
                
                if not suffix_removed(word):
                    word = remove_vowel(word)
                    
            word = remove_accents(word)
            
            stemmed_words.append(word)
            
        print(stemmed_words)
        
if __name__ == '__main__':
	init()