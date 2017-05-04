#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def main():
    class_probs = dict()
    amount_docs = 0
    
    for line in sys.stdin:
        amount_docs += 1
        
        doc = line.rstrip("\r\n").strip().split(" ")
        cl = doc.pop(0)
        
        try:
            class_probs[cl] += 1
        except:
            class_probs[cl] = 1
        
    for cl in class_probs:
        class_probs[cl] /= amount_docs
        
    print(class_probs)


if __name__ == '__main__':
	main()