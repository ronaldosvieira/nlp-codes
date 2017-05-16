#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Document(object):
    def __init__(self, cl, words):
        self.cl = cl
        self.words = words
        
    def get_class(self):
        return self.cl
        
    def get_words(self):
        return self.words
        
class DocRepository(object):
    def __init__(self):
        self.classes = dict()
        self.docs = list()
        
    def get_classes(self):
        return list(self.classes.keys())
        
    def get_docs(self):
        return self.docs
        
    def class_probs(self, cl):
        return self.classes[cl]['count'] / self.amount_docs();
        
    def class_vocab(self, cl):
        return self.classes[cl]['vocab'];
        
    def amount_docs(self):
        return len(self.docs)
        
    def amount_classes(self):
        return len(self.classes.keys())
        
    def __add_class(self, cl):
        self.classes[cl] = {'count': 0, 'vocab': set()}
        
    def add_doc(self, doc):
        if isinstance(doc, Document):
            self.docs.append(doc)
            
            cl = doc.get_class()
            
            if cl not in self.classes:
                self.__add_class(cl)
            
            self.classes[cl]['count'] += 1
            self.classes[cl]['vocab'].update(doc.get_words())
        else:
            raise Exception('not a document bro')