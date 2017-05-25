#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

class Document(object):
    def __init__(self, cl, words):
        self.cl = cl
        self.words = words
        
    def get_class(self):
        return self.cl
        
    def get_words(self):
        return self.words
        
class Model(object):
    def __init__(self):
        self.classes = dict()
        self.docs = list()
        self.probs = dict()
        self.len_vocab = set()
        
    def get_classes(self):
        return list(self.classes.keys())
        
    def get_docs(self):
        return self.docs
        
    def class_probs(self, cl):
        return self.classes[cl]['doc_count'] / self.amount_docs()
        
    def get_len_vocab(self):
        if self.len_vocab is None:
            vocab = list()
            
            [vocab.extend(list(self.classes[cl]['vocab'].keys()))
                for cl in self.classes]
                
            self.len_vocab = len(set(vocab))
            
        return self.len_vocab
        
    def word_count(self, cl):
        return self.classes[cl]['word_count']
        
    def cond_probs(self, cl, word):
        try:
            word_freq = self.classes[cl]['vocab'][word]
        except:
            word_freq = 0
        
        word_count = self.word_count(cl)
            
        # without laplace smoothing
        # return word_freq / word_count
        
        # with laplace smoothing (add-1)
        return (word_freq + 1) / (word_count + self.get_len_vocab())
        
    def amount_docs(self):
        return len(self.docs)
        
    def amount_classes(self):
        return len(self.classes.keys())
        
    def __add_class(self, cl):
        self.classes[cl] = {'doc_count': 0, 'word_count': 0, 'vocab': dict()}
        
    def add_doc(self, doc):
        if isinstance(doc, Document):
            self.probs.clear()
            self.len_vocab = None
            
            self.docs.append(doc)
            
            cl = doc.get_class()
            
            if cl not in self.classes:
                self.__add_class(cl)
            
            self.classes[cl]['doc_count'] += 1
            self.classes[cl]['word_count'] += len(doc.get_words())
            
            for word in doc.get_words():
                try:
                    self.classes[cl]['vocab'][word] += 1
                except:
                    self.classes[cl]['vocab'][word] = 1
        else:
            raise Exception('not a document bro')
    
    def classify(self, sentence):
        tokens = sentence.rstrip("\r\n").strip().split(" ")
        results = dict()
        
        for cl in self.get_classes():
            for token in tokens:
                try:
                    self.probs[(token, cl)]
                except:
                    self.probs[(token, cl)] = self.cond_probs(cl, token)
        
        for cl in self.get_classes():
            results[cl] = math.log(self.class_probs(cl))
            
            for token in tokens:
                results[cl] += math.log(self.probs[(token, cl)])
                
            results[cl] = math.exp(results[cl])

        return results
        
class Confusion(object):
    def __init__(self, classes, results):
        self.classes = classes
        self.results = results
        
        self.classes.sort()
        self.__confusion = dict()
        
        for cl in self.classes:
            self.__confusion[cl] = dict()
            
            for cl2 in classes:
                self.__confusion[cl][cl2] = 0
        
        for truth, predicted in results:
            self.__confusion[truth][predicted] += 1
    
    def __str__(self):
        out = "TxP"
        
        for cl in self.classes:
            out += "\t'" + cl + "'"
            
        out += "\n"
            
        for cl in self.classes:
            out += "'" + cl + "'"
            
            for cl2 in self.classes:
                out += "\t" + str(self.__confusion[cl][cl2])
                
            out += "\n"
            
        return out
    
    def tp(self, cl):
        return self.__confusion[cl][cl]
    
    def tn(self, cl):
        return sum(self.__confusion[cl2][cl2] 
            for cl2 in self.classes if cl2 != cl)
    
    def fp(self, cl):
        return sum(self.__confusion[cl2][cl]
            for cl2 in self.classes if cl2 != cl)
    
    def fn(self, cl):
        return sum(self.__confusion[cl][cl2]
            for cl2 in self.classes if cl2 != cl)
    
    def precision(self, cl):
        return self.tp(cl) / (self.tp(cl) + self.fp(cl))
        
    def recall(self, cl):
        return self.tp(cl) / (self.tp(cl) + self.fn(cl))
    
    def accuracy(self):
        return sum(self.__confusion[cl][cl] 
            for cl in self.classes) / len(self.results)