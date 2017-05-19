#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from documents import Document, Model

def main():
    doc_rep = Model()
    
    for line in sys.stdin:
        doc = line.rstrip("\r\n").strip().split(" ")
        cl = doc.pop(0)
        
        doc_rep.add_doc(Document(cl, doc))
    
    for cl in doc_rep.get_classes():
        print(cl)
        print(doc_rep.class_probs(cl))
        print(doc_rep.cond_probs(cl, 'Chinese'))

if __name__ == '__main__':
	main()