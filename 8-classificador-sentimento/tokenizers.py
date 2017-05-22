#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def tokenize(text):
	text = re.sub(r"[(\r+)(\n+)(\t+)]", " ", text)
	tokens = list()
	
	for pre_token in re.split(r"\s+", text):
		split_token = [i for i in re.split(r"([^\w\d]$)", pre_token) if len(i) > 0]
		
		tokens = tokens + split_token
	
	return tokens

def sentence_tokenize(text):
	text = re.sub(r"[(\r+)(\n+)(\t+)]", " ", text)
	sentences = list()
	
	pre_tokens = re.split(r"([\.\;\?\!\:]+)", text)
	
	for p in range(0, len(pre_tokens) - 2, 2):
		sentences.append( pre_tokens[p] +  pre_tokens[p+1] )
	
	return sentences