#!/usr/bin/env python
# -*- coding: utf-8 -*-

def rule(path="rules/step0.pt"):
    file = open(path, "r", encoding="utf8")
    lines = file.readlines()
    
    rules = dict()
    
    for i in range(1, len(lines)):
        tokens = lines[i].replace("\"", "").replace("\n", "").replace("\r", "").split("\t")
        
        exceptions = list()
        
        if "*" not in tokens[3]:
            exceptions = tokens[3].split(",")

        rules[tokens[0]] = (tokens[2], int(tokens[1]), exceptions)
        
    return rules
    
if __name__ == '__main__':
	rule()