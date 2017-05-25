#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from random import shuffle
from documents import *
from tokenizers import tokenize
from preprocessors import sentimentify, negation

def main():
    model = Model()
    docs = list()
    
    preprocess = True
    
    if preprocess:
        for line in sys.stdin:
            tokens = negation(sentimentify(tokenize(line)))
            docs.append(Document(tokens[0], set(tokens[1:])))
    else:
        for line in sys.stdin:
            tokens = tokenize(line)
            docs.append(Document(tokens[0], set(tokens[1:])))
    
    shuffle(docs)
    
    train = docs[:int(len(docs) * .8)]
    test = docs[len(train):]
    
    [model.add_doc(doc) for doc in train]
    
    results = list()
    
    for doc in test:
        result = model.classify(" ".join(doc.get_words()))
        
        results.append((max(result, key=result.get), doc.get_class()))
        
    confusion = Confusion(model.get_classes(), results)
    
    print(confusion)
    print(confusion.mae())
    print(confusion.rmse())
    
    print("Precision-1: ", confusion.precision('1'))
    print("Precision-2: ", confusion.precision('2'))
    print("Precision-3: ", confusion.precision('3'))
    print("Precision-4: ", confusion.precision('4'))
    print("Precision-5: ", confusion.precision('5'))

if __name__ == '__main__':
	main()