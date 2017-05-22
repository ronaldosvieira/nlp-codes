#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from random import shuffle
from documents import Document, Model
from tokenizers import tokenize

def main():
    model = Model()
    docs = list()
    
    preprocess = None
    
    if preprocess:
        for line in sys.stdin:
            pass
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

    precision = sum(1 for res in results if res[0] == res[1])
    
    print("Precision: ", precision / len(results))

if __name__ == '__main__':
	main()