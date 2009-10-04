#! /usr/bin/env python
import cPickle as pickle
import os.path

f = open('.figleaf')
d = pickle.load(f)
f.close()

d2 = {}
for key,val in d.items():
    if key.endswith('.py'):
        key = os.path.normpath(key)
    d2[key] = val

f = open('.figleaf', 'w')
pickle.dump(d2, f)
f.close()

