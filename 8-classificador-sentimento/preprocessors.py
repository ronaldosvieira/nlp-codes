#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tokenizers import tokenize

lexicon = None
negations = None

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

def get_negations(path='lexicon/negations.lex'):
	global negations
	
	if negations is None:
		negations = dict()
		
		with open(path, 'r') as file:
			lines = file.readlines()
			
		for line in lines:
			negations[line.rstrip("\r\n")] = True
			
	return negations

def sentimentify(tokens, lex=get_lexicon()):
	for i in range(len(tokens)):
		try:
			tokens[i] = lex[tokens[i]]
		except:
			pass # Beleza!
	return tokens

def negation(tokens, lex=get_negations()):
	for i in range(len(tokens)):
		try:
			lex[tokens[i]]
		
			for j in range(i, len(tokens)):
				if tokens[j] not in ".;?!:":
					tokens[j] = "not_" + tokens[j]
				else:
					break
		except:
			pass # Beleza!
		
	return tokens
	