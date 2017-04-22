#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import unicodedata
import os.path
import termios
import fcntl
import curses
from ast import literal_eval
import operator

model_2_gram = dict()
model_3_gram = dict()

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

def load_dataset(path="dataset/critica/mact01.txt"):
	try:
		file = open(path, "r", encoding="utf8")
		text = file.read()
		file.close()
		return text
	except UnicodeDecodeError:
		file = open(path, "r", encoding="latin1")
		text = file.read()
		file.close()
		file = open(path, "w")
		file.write(text)
		file.close()
		return text

def myGetch():
	fd = sys.stdin.fileno()

	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)

	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

	try:        
		while 1:            
			try:
				c = sys.stdin.read(1)
				if c != "":
					return c
			except IOError: pass
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

def check_models():
	if not os.path.exists("models/2-gram"):
		print("Criando modelo para 2-gram")
		create_model_2_gram()
		print("Pressione qualquer tecla para continuar")
		myGetch()

	if not os.path.exists("models/3-gram"):
		print("Criando modelo para 3-gram")
		create_model_3_gram()
		print("Pressione qualquer tecla para continuar")
		myGetch()

def init_prediction():
	load_model()
	c = ""
	sentence = ""
	stdscr = curses.initscr()
	
	while c != "\n":
		try:
			suggs = ""
			if c == " ":
				suggs = suggestions(sentence)
				stdscr.clear()
			stdscr.addstr(0, 0, "Pressione ENTER para sair")
			if len(suggs) >= 3:
				stdscr.addstr(2, 0, "Top Suggestions: {}".format(suggs[0:3]))
			if len(suggs) >= 1:
				stdscr.addstr(3, 0, "Best Suggestion: {}".format(suggs[0:1]))
			stdscr.addstr(5, 0, "Sentence: {}".format(sentence))
			stdscr.refresh()
			
			c = myGetch()
			if c == '\x08' or c == '\x7f':
				sentence = sentence[0:len(sentence)-1]
				stdscr.clear()
			else:
				sentence += c

		except KeyboardInterrupt:
			curses.nocbreak()
			curses.echo()
			curses.endwin()
			exit(1)
		finally:
			curses.nocbreak()
			curses.echo()
			curses.endwin()

def load_model():
	if len(model_2_gram) > 0 and len(model_3_gram) > 0:
		return None
	
	file = open("models/2-gram", "r")
	lines = file.readlines()
	file.close()
	
	for l in lines:
		tk = l.split("\t")
		model_2_gram[literal_eval(tk[0])] = float(tk[1].replace("\n", ""))
	
	file = open("models/3-gram", "r")
	lines = file.readlines()
	file.close()
	
	for l in lines:
		tk = l.split("\t")
		model_3_gram[literal_eval(tk[0])] = float(tk[1].replace("\n", ""))

def suggestions(sentence=""):
	load_model()
	tokens = tokenize(sentence)
	sugg = dict()	
	
	if len(tokens) == 0:
		return sugg
	
	list_1 = list()
	list_2 = list()
	
	if len(tokens) > 2:
		print("Usando 3-gram")
		for k in model_3_gram:
			if tokens[-2] == k[0] and tokens[-1] == k[1]:
				list_1.append(k)
			elif len(tokens) >= 3 and tokens[-3] == k[0] and tokens[-2] == k[1]:
				list_2.append(k)
	
		if len(list_1) > 0:
			for s in list_1:
				if model_3_gram[s] > 0.0:
					sugg[s[2]] = model_3_gram[s]
		elif len(list_2) > 0:
			for s in list_2:
				if model_3_gram[s] > 0.0:
					sugg[s[2]] = model_3_gram[s]
	
	list_1 = list()
	list_2 = list()
	if len(tokens) <= 2 or len(sugg) == 0:
		print("Usando 2-gram")
		for k in model_2_gram:
			if tokens[-1] == k[0]:
				list_1.append(k)
			elif len(tokens) >= 2 and tokens[-2] == k[0]:
				list_2.append(k)
	
		if len(list_1) > 0:
			for s in list_1:
				if model_2_gram[s] > 0.0:
					sugg[s[1]] = model_2_gram[s]
		elif len(list_2) > 0:
			for s in list_2:
				if model_2_gram[s] > 0.0:
					sugg[s[1]] = model_2_gram[s]
		
	sorted_sugg = sorted(sugg.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_sugg

def create_model_2_gram(n_datasets=45):
	
	file = open("models/2-gram", "w")
	model = dict()
	count = dict()
	
	for f in range(1, n_datasets + 1):
		dataset_path = "dataset/critica/mact" + "%02d" % (f) + ".txt"
		print("Gerando modelo do dataset: %s" % (dataset_path))

		text = load_dataset(dataset_path)
		sentences = sentence_tokenize(text)
		
		for s in sentences:
			tokens = tokenize(s)
			
			for pc in tokens:
				try:
					count[pc] += 1
				except:
					count[pc] = 1
				
			inserted = dict()
			for t1 in range(len(tokens)):
				for t2 in range(t1, len(tokens)):
					
					occurences = sum(1 for i in range(len(tokens)) if tokens[i:i+2]==[tokens[t1], tokens[t2]])
					key = (tokens[t1], tokens[t2])
					
					try:
						try:
							inserted[key]
						except:
							model[key] = model[key] + occurences
							inserted[key] = True
					except:
						model[key] = occurences
						inserted[key] = True

	for m in model:
		prob = model[m]/count[m[0]]
		file.write(str(m) + "\t" + str(prob) + "\n")
		file.flush()
	
	file.close()

def create_model_3_gram(n_datasets=45):
	
	file = open("models/3-gram", "w")
	model = dict()
	count = dict()
	
	for f in range(1, n_datasets + 1):
		dataset_path = "dataset/critica/mact" + "%02d" % (f) + ".txt"
		print("Gerando modelo do dataset: %s" % (dataset_path))

		text = load_dataset(dataset_path)
		sentences = sentence_tokenize(text)
		
		for s in sentences:
			tokens = tokenize(s)
			
			for pc in range(len(tokens) - 1):
				try:
					count[(tokens[pc], tokens[pc + 1])] += 1
				except:
					count[(tokens[pc], tokens[pc + 1])] = 1
			
			inserted = dict()
			for t1 in range(len(tokens)):
				for t2 in range(t1 + 1, len(tokens)):
					
					occurences = sum(1 for i in range(len(tokens)) if tokens[i:i+3]==[tokens[t1], tokens[t1 + 1], tokens[t2]])
					key = (tokens[t1], tokens[t1 + 1], tokens[t2])

					try:
						try:
							inserted[key]
						except:
							model[key] = model[key] + occurences
							inserted[key] = True
					except:
						model[key] = occurences
						inserted[key] = True

	for m in model:
		prob = model[m]/count[(m[0], m[1])]
		file.write(str(m) + "\t" + str(prob) + "\n")
		file.flush()
	
	file.close()

def main():
	
	check_models()
	init_prediction()
	

if __name__ == '__main__':
	main()