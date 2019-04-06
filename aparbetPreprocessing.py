# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 22:58:05 2019

@author: 13982
"""
import re, numpy as np, keras

# assign a unique index for each unique character in word
def assignCharIndex(char_index, char, index_tracker):
    if char not in char_index:
        char_index[char] = index_tracker
        index_tracker += 1
    return index_tracker

tr = input("training data: ")
dv = input("dev data: ")

training_prepare = open(tr+'.txt', encoding = 'utf-8')
num_example = 0

"""Assign character 'PADD' with integer encoding of 0"""
char_index = {}
phone_index = {}
char_index['PADD'] = 0
phone_index['PADD'] = 0
char_tracker = 1
phone_tracker = 1

char_set = set()
phone_set = set()
char_set.add('PADD')
phone_set.add('PADD')

for line in training_prepare:       
    if line[:3] == ';;;':
        continue
    data = re.sub(' +', ' ', line)
    data = data.split()
    word, phone = data[0], data[1:]
    phone = ''.join(phone)
    
    """This deletes the (number) in word, and tonal representation in phones"""
    """Not necessarily true, remove if not needed"""
    word, phone = re.sub('\(\d*\)', '', word), re.sub('\d*', '', phone)
    
    for ch in word:
        char_tracker = assignCharIndex(char_index, ch, char_tracker)
        char_set.add(ch)
    for ch in phone:
        phone_tracker = assignCharIndex(phone_index, ch, phone_tracker)
        phone_set.add(ch)
    
#    print(word + '        ', end='')
#    print(phone)
    
    num_example += 1
    len_word = len(word)
    len_phone = len(phone)

print(num_example)
training_prepare.close()

"""Get the 98th percentile word and phone length"""
max_word_len = int(np.percentile(len_word, 98))
max_phone_len = int(np.percentile(len_phone, 98))

# Making 3D input matrix of zeros with corresponding axes
input_matrix = np.zeros((num_example, max_word_len, len(char_set)))
# Making 3D output matrix of zeros with corresponding axes
output_matrix = np.zeros((num_example, max_phone_len, len(phone_set)))



training = open(tr+'.txt', encoding = 'utf-8')

"""length_tracker to identify the current character index in word of concern"""
length_tracker = 0

example_id = 0

for line in training:
    if line[:3] == ';;;':
        continue
    data = re.sub(' +', ' ', line)
    data = data.split()
    word, phone = data[0], data[1:]
    phone = ''.join(phone)
    word, phone = re.sub('\(\d*\)', '', word), re.sub('\d*', '', phone)
    
    for ch in word:
        """Row i column j axis k is 1 if the jth character in word i has integer encoding k"""
        if length_tracker < max_word_len:
            int_encoding = char_index[ch]
            input_matrix[example_id][length_tracker][int_encoding] = 1
            length_tracker += 1
    """Add PADD character"""
    if len(word) < max_word_len:
        for l in range(length_tracker, max_word_len):
            input_matrix[example_id][l][0] = 1
    
    length_tracker = 0
    
    for ch in phone:
        """Row i column j axis k is 1 if the jth character in lemma i has integer encoding k"""
        if length_tracker < max_phone_len:
            int_encoding = phone_index[ch]
            output_matrix[example_id][length_tracker][int_encoding] = 1
            length_tracker += 1
    """Add PADD character"""
    if len(word) < max_phone_len:
        for l in range(length_tracker, max_phone_len):
            output_matrix[example_id][l][0] = 1
    
    length_tracker = 0
    example_id += 1
    
    
    
    
    
    
    

