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
    k_fold = 5
    
    if preprocess:
        for line in sys.stdin:
            tokens = negation(sentimentify(tokenize(line)))
            docs.append(Document(tokens[0], set(tokens[1:])))
    else:
        for line in sys.stdin:
            tokens = tokenize(line)
            docs.append(Document(tokens[0], set(tokens[1:])))
    
    # shuffle(docs)

    results = list()
    step = int(len(docs) / k_fold)
    
    for k in range(0, len(docs), step):
        train = docs[0:k] + docs[k + step:len(docs)]
        test = docs[k:k + step]
    
        [model.add_doc(doc) for doc in train]
        
        for doc in test:
            result = model.classify(" ".join(doc.get_words()))
            
            results.append((max(result, key=result.get), doc.get_class()))
            
    confusion = Confusion(model.get_classes(), results)
    
    print(confusion)

if __name__ == '__main__':
	main()