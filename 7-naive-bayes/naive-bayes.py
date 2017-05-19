#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from documents import Document, Model

def main():
    model = Model()
    
    for line in sys.stdin:
        doc = line.rstrip("\r\n").strip().split(" ")
        cl = doc.pop(0)
        
        model.add_doc(Document(cl, doc))
    
    print(model.classify("Chinese Chinese Chinese Tokyo Japan"))

if __name__ == '__main__':
	main()