import numpy as np
import os
import sys
import re
import random
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
import pickle
#from keras.preprocessing.sequence import pad_sequences


def overview_selected_files(path, file_ending):
	'''
	Overview ..
	'''
	for file in os.listdir(path):
		if file.endswith(file_ending):
			print(os.path.join('found files :', file)) 
				
            
def paths_selected_files(path, file_ending):
    '''
    Get paths for selected files
    '''
    path_books_list = [os.path.join(path, file) 
                       for file in os.listdir(path) if file.endswith(file_ending)]
    print(path_books_list)
    return path_books_list


def open_book_list(path_books_list):
    '''
    Open book list
    '''
    book_list = [open(file).read() for file in path_books_list]
    
    [print('Book #{book_n} has a word length of {book_text}'.format(
    book_n=book_n, book_text=len(book_text))) 
                     for book_n, book_text in enumerate(book_list)]
    return book_list


def to_token(book_list, stopwords_threshold):
    book_list_tokenize = [word_tokenize(book) for book in book_list]
    book_token = [token for book in book_list_tokenize for token in book]
    words = [word.lower() for word in book_token if word.isalpha()]
    nltk_stopwords = stopwords.words('english')
    nltk_stopwords = [stopword for stopword in nltk_stopwords if not int(len(stopword)) > stopwords_threshold]
    words = [word for word in words if not word in nltk_stopwords]
    return words

def remove_roman_num_chars(words, pattern):
    words_remove = [re.findall(pattern, word) for word in words]
    words_remove = [word for list_ in words_remove for word in list_]
    words_remove = set(words_remove)
    words = [word for word in words if not word in words_remove]
    return words

def creating_dicts(words):
    chars = sorted(list(set(' '.join(words))))[1:]
    index_to_char = dict((nr+1, char) for nr,char in enumerate(chars))
    char_to_index = dict((char, nr+1) for nr,char in enumerate(chars))
    return index_to_char, char_to_index

def word_to_char_encoding(words, char_to_index_dict):
    words_char = [list(word) for word in words]
    words_char_index = [[char_to_index[char] for char in list_in_list] for list_in_list in words_char]
    return words_char_index


def random_letter_exchange(words_char_index):
    words_char_index_rand = [random.randint(0, len(word_char_index) -1) for word_char_index in words_char_index]
    
    words_char_index_corrupted = []
    for word_char_index, random_index in zip(words_char_index, words_char_index_rand):
        word_char_index_copy = word_char_index.copy()
        word_char_index_copy[random_index] = np.random.randint(0, len(char_to_index))
        words_char_index_corrupted.append(word_char_index_copy)
        
    return words_char_index_corrupted


def placeholder(words_char_index, char_to_index):
    words_char_length = [len(word) for word in words_char_index]
    
    num_samples = len(words_char_index)
    max_len = int(round(np.array(words_char_length).mean() +(3*np.array(words_char_length).std()),0))
    char_len = int(len(char_to_index)) + 1
    placeholder_3d = np.zeros((num_samples, max_len, char_len), dtype=np.bool) 
    print(placeholder_3d.shape)
    return placeholder_3d


def padding_x_y(words_char_index, words_char_index_corrupted, max_len):
    
    words_char_index_pad = pad_sequences(words_char_index, max_len)
    words_char_index_corrupted_pad = pad_sequences(words_char_index_corrupted, max_len)
    return words_char_index_pad, words_char_index_corrupted_pad

def clean_text(text):
    '''Remove unwanted characters and extra spaces from the text'''
    text = re.sub(r'\n', ' ', text) 
    text = re.sub(r'[{}@_*>()\\#%+=\[\]~~ᵒ·┌í×ö⁄&üŒ½âàÆîû┼└çÖºê$∞œ°│Üä…ÉÈïñ£ô–]','', text) # TODO: add ÆØÅ + diacritics
    text = re.sub('a0','', text)
    text = re.sub('\'92t','\'t', text)
    text = re.sub('\'92s','\'s', text)
    text = re.sub('\'92m','\'m', text)
    text = re.sub('\'92ll','\'ll', text)
    text = re.sub('\'91','', text)
    text = re.sub('\'92','', text)
    text = re.sub('\'93','', text)
    text = re.sub('\'94','', text)
    text = re.sub('\.','. ', text)
    text = re.sub('\!','! ', text)
    text = re.sub('\?','? ', text)
    text = re.sub(' +',' ', text)
    text = re.sub('\ufeff',' ', text)
    text = re.sub('’',"'", text)
    text = re.sub('“','"', text)
    text = re.sub('”','"', text)
    text = re.sub(r'www.*?\s',' ', text) # Todo: fix
    return text

def save_pickle(object, path, name):
    with open(path + name + '.pkl','wb') as f:
        pickle.dump(object, f, pickle.HIGHEST_PROTOCOL)
        
def load_pickle(path, name):
    with open(path + name + '.pkl','rb') as f:
        return pickle.load(f)