#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tokenizers import tokenize

lexicon = None

def get_lexicon(path='lexicon/lexicon.lex'):
	global lexicon
	
	if lexicon is None:
		lexicon = dict()
		lines = list()
		
		with open(path, 'r') as file:
			lines = file.readlines()
		
		for line in lines:
			lexicon[tokenize(line)[2].split("=")[1]] = tokenize(line)[0].split("=")[1] + tokenize(line)[5].split("=")[1]
	
	return lexicon
	
def sentimentify(tokens, lex=get_lexicon()):
	for i in range(len(tokens)):
		try:
			tokens[i] = lex[tokens[i]]
		except:
			pass # Beleza!
	return tokens
