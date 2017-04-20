#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from read_rule import rule

def reduction(dataset, word):
    matches = [suffix 
        for suffix in dataset.keys() 
            if word[-len(suffix):] == suffix 
                and word not in dataset[suffix][2]
                and len(word[:-len(suffix)]) >= dataset[suffix][1]]
    
    if matches:
        suffix = matches[0]
        
        word = word[:-len(suffix)] + dataset[suffix][0]
    
    return word
    
def plural_reduction(word):
    return reduction(rule("rules/step0.pt"), word)

def feminine_reduction(word):
    return reduction(rule("rules/step1.pt"), word)
    
def augmentative_reduction(word):
    return reduction(rule("rules/step3.pt"), word)
    
def adverb_reduction(word):
    return reduction(rule("rules/step2.pt"), word)
    
def noun_reduction(word):
    return reduction(rule("rules/step4.pt"), word)

def suffix_removed(new_word, old_word):
    return new_word != old_word

def verb_reduction(word):
    return reduction(rule("rules/step5.pt"), word)

def remove_vowel(word):
    return reduction(rule("rules/step6.pt"), word)

def remove_accents(word):
    return reduction({}, word)

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
            old_word = adverb_reduction(word)
            new_word = noun_reduction(old_word)
            
            if not suffix_removed(new_word, old_word):
                old_word = new_word
                new_word = verb_reduction(new_word)
                
                if not suffix_removed(new_word, old_word):
                    new_word = remove_vowel(new_word)
                    
            new_word = remove_accents(new_word)
            
            stemmed_words.append(new_word)
            
        print(''.join(stemmed_words))
        
if __name__ == '__main__':
	init()