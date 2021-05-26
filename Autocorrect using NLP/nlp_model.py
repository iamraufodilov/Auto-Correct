# load libraries
import re
from collections import Counter
import numpy as np
import pandas as pd
import itertools


# loading and preprocessing data
def process_data(file_name):
    words = [] 
    with open(file_name) as f:
        file_name_data = f.read()
        file_name_data=file_name_data.lower()
        words = re.findall(r'\w+',file_name_data)

    return words

word_l = process_data('G:/rauf/STEPBYSTEP/Projects/NLP/Auto Correct/Autocorrect using NLP/shakespeare.txt')
vocab = set(word_l)
five_part = set(itertools.islice(vocab, 5)) # just to see five example from vocabulary
#_>print(five_part)


# create count dictionary for words and their occurence
def get_count(word_l):
    word_count_dict = {}  # fill this with word counts
    word_count_dict = Counter(word_l)
    return word_count_dict

word_count_dict = get_count(word_l)
small_part = dict(itertools.islice(word_count_dict.items(), 5)) # lets look five example from list
#_>print(small_part)

# get dictionary with words and their probbility in text
def get_probs(word_count_dict):
    probs = {}  # return this variable correctly
    
    m = sum(word_count_dict.values())
    for key in word_count_dict :
        probs[key] = word_count_dict[key]/m
    return probs

probs = get_probs(word_count_dict)
small_part2 = dict(itertools.islice(probs.items(), 5)) # lets look 5 examples from dict
#_>print(small_part2)


# delete word
def delete_letter(word):
    delete_l = []
    split_l = []

    for i in range(len(word)):
        split_l.append([word[:i],word[i:]])
    for a,b in split_l :
        delete_l.append(a+b[1:])

    return delete_l


# switch the word
def switch_letter(word):
    switch_l = []
    split_l = []

    for c in range(len(word)):
        split_l.append([word[:c],word[c:]])
    switch_l = [a + b[1] + b[0] + b[2:] for a,b in split_l if len(b) >= 2]    

    return switch_l


# replce the word
def replace_letter(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    replace_l = []
    split_l = []

    for c in range(len(word)):
        split_l.append((word[0:c],word[c:]))
    replace_l = [a + l + (b[1:] if len(b)> 1 else '') for a,b in split_l if b for l in letters]
    replace_set=set(replace_l)    
    replace_set.remove(word)
    # turn the set back into a list and sort it, for easier viewing
    replace_l = sorted(list(replace_set))

    return replace_l


# insert word
def insert_letter(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_l = []
    split_l = []

    for c in range(len(word)+1):
        split_l.append((word[0:c],word[c:]))
    insert_l = [ a + l + b for a,b in split_l for l in letters]

    return insert_l


# edit one letter at a time
def edit_one_letter(word, allow_switches = True):
    edit_one_set = set()

    edit_one_set.update(delete_letter(word))
    if allow_switches:
        edit_one_set.update(switch_letter(word))
        edit_one_set.update(replace_letter(word))
        edit_one_set.update(insert_letter(word))

    return edit_one_set


# edit two letter at a time
def edit_two_letters(word, allow_switches = True):
    edit_two_set = set()

    edit_one = edit_one_letter(word,allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w,allow_switches=allow_switches)
            edit_two_set.update(edit_two)

    return edit_two_set


# to get best word
def get_corrections(word, probs, vocab, n=2):    
    suggestions = []
    n_best = []

    suggestions = list((word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(vocab))
    n_best = [[s,probs[s]] for s in list(reversed(suggestions))]

    return n_best


# test our model
my_word = 'dys' 
tmp_corrections = get_corrections(my_word, probs, vocab, 2) 
for i, word_prob in enumerate(tmp_corrections):
    print(f"word {i}: {word_prob[0]}, probability {word_prob[1]:.6f}") # wow we tested our model prefectly it suggested three word with respective probability


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# CONCLUSION
'''
in this project we load txt dataset
and we get vocabulary and probability of word in that text
we created function to delete edit replace and insert functions
finally we tested our model with probaibility result
'''