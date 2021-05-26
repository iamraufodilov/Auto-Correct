# load libraries
import re
from collections import Counter
import numpy as np
import pandas as pd


# load dataset
def process(fname):
    words = [] 
    with open(fname) as fl:
        data = fl.read()
    data = data.lower()
    words = re.findall('\w+',data)    
    return words

words = process('G:/rauf/STEPBYSTEP/Projects/NLP/Auto Correct/Auto Correction Implementation/shakespeare.txt')
vocab = set(words)

def count(words):
    countd = {}  
    countd = Counter(words)          
    return countd

count_dict = count(words)

def probabilities(count_dict):
    p = {} 
    l = sum(count_dict.values())
    for k in count_dict.keys():
        p[k] = count_dict[k] / l    
    return p
probs = probabilities(count_dict)


def delete(word):    
    d = []
    s = []
    for i in range(len(word)):
        s.append((word[:i],word[i:]))
    for j,k in s:
        d.append(j+k[1:])    
    return d

def switch(word):   
    sw = []
    sp = []
    l=len(word)    
    for i in range(l):
        sp.append((word[:i],word[i:]))
    sw = [j + k[1] + k[0] + k[2:] for j,k in sp if len(k) >= 2]     
    return sw

def replace(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    r = []
    s = []
    for i in range(len(word)):
        s.append((word[0:i],word[i:]))
    r = [j + l + (k[1:] if len(k)> 1 else '') for j,k in s if k for l in letters]
    rs=set(r)    
    r = sorted(list(rs))      
    return r

def insert(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    i = []
    s = []
    for j in range(len(word)+1):
        s.append((word[0:j],word[j:]))
    i = [ m + l + n for m,n in s for l in letters] 
    return i

def edit1(word): 
    edit1s = set()
    edit1s.update(delete(word))
    edit1s.update(replace(word))
    edit1s.update(insert(word))
    edit1s.update(switch(word))
    return edit1s

def edit2(word):   
    edit2s = set()
    edit_one = edit1(word)
    for w in edit_one:
        if w:
            edit_two = edit1(w)
            edit2s.update(edit_two)
    return edit2s


def correct(word, probs, vocab, n=2):

    suggestions = []
    n_best = []
    suggestions = list((word in vocab and word) or edit1(word).intersection(vocab) or edit2(word).intersection(vocab))
    n_best = [[s,probs[s]] for s in list(reversed(suggestions))] 
    print("input word = ", word, "\nsuggestions = ", suggestions)
    return n_best

my_word = 'nme' 
corrections = correct(my_word, probs, vocab, 4)


