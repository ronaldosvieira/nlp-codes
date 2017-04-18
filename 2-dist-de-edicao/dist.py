#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

first = raw_input()
second = raw_input()

dist = np.empty(shape=(len(first) + 1, len(second) + 1), dtype=np.int32)

dist[:, 0] = range(0, dist.shape[0])
dist[0, :] = range(0, dist.shape[1])

for j in range(1, dist.shape[1]):
    for i in range(1, dist.shape[0]):
        penalty = 2 if first[i - 1] != second[j - 1] else 0
        
        top = dist[i - 1, j] + 1
        left = dist[i, j - 1] + 1
        diag = dist[i - 1, j - 1] + penalty
        
        dist[i, j] = min(top, left, diag)

print(dist[-1, -1])