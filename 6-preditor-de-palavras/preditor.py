#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import unicodedata
import os.path
import termios
import fcntl
import curses

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

def remove_accents(word):
	return "".join((c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn'))

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
	if not os.path.exists("models/2_grams"):
		print("Criando modelo para 2_grams")
		create_model(2)
		print("Pressione qualquer tecla para continuar")
		myGetch()

	if not os.path.exists("models/3_grams"):
		print("Criando modelo para 3_grams")
		create_model(3)
		print("Pressione qualquer tecla para continuar")
		myGetch()

def init_prediction():
	c = ""
	sentence = ""
	stdscr = curses.initscr()
	
	while c != "\n":
		try:
			stdscr.addstr(0, 0, "Pressione ENTER para sair")
			stdscr.addstr(2, 0, "Top Suggestions: {}".format(suggestions()[0:3]))
			stdscr.addstr(3, 0, "Best Suggestion: {}".format(suggestions()[0:1]))
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

def load_model(path="dataset/models/2_grams"):
	pass

def suggestions(sentence=""):
	sugg = [["Exemplo1", 0.9], ["Exemplo2", 0.65]]
	return sugg

def create_model_2_gram(n_datasets=45):
	
	file = open("models/2-gram", "w")
	
	for f in range(1, n_datasets + 1):
		dataset_path = "dataset/critica/mact" + "%02d" % (f) + ".txt"
		print("Gerando modelo do dataset: %s" % (dataset_path))
		
		model = dict()
		text = load_dataset(dataset_path)
		sentences = sentence_tokenize(text)
		
		for s in sentences:
			tokens = tokenize(s)
			inserted = dict()
			for t1 in range(len(tokens)):
				for t2 in range(t1, len(tokens)):
					
					occurences = sum(1 for i in range(len(tokens)) if tokens[i:i+2]==[tokens[t1], tokens[t2]])
					key = tokens[t1] + " -> " + tokens[t2]
					
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
			file.write(m + " " + str(model[m]) + "\n")
			file.flush()
	
	file.close()
	

def main():
	
	# check_models()
	# init_prediction()
	
	create_model_2_gram()

		
		
if __name__ == '__main__':
	main()