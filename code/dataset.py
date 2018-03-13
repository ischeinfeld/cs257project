import re
import random
from itertools import product
from itertools import islice
from string import ascii_letters

import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

class Dataset:
    def __init__(self, regex_max_length, string_max_length, alphabet, regex_chars):
        self.regex_max_length = regex_max_length
        self.string_max_length = string_max_length
        self.alphabet = alphabet
        self.regex_chars = regex_chars

        self.regex_char_int = {c: i + 1 for i, c in enumerate(alphabet + regex_chars)}
        self.string_char_int = {c: i + 1 for i, c in enumerate(alphabet)}
        self.regex_int_char = "_" + alphabet + regex_chars
        self.string_int_char = "_" + alphabet

    def gen(self, random_frac = None):
        return dataset_generator(self.regex_max_length, self.string_max_length, self.alphabet, self.regex_chars, random_frac)

    def bound_size(self):
        return triple_count_bound(self.regex_max_length, self.string_max_length, self.alphabet, self.regex_chars)



def all_strings(max_length, alphabet):
    """Returns a generator of all strings up to a given length from an alphabet"""
    for length in range(max_length + 1):
        for s in product(alphabet, repeat=length):
            yield ''.join(s)

def add_slash(c):
    try:
        integer = int(c)
        return "\\" + c
    except:
        return c

def backref(s):
    return "".join([add_slash(c) for c in s])

def extract_valid_regexes(candidates):
    """Takes a generator of strings and returns a generator of compiled valid regexes"""
    for c in candidates:
        try:
            yield re.compile(backref(c))
        except:
            pass

def all_regexes(max_length, alphabet):
    """Returns a generator of all valid regexes up to a length from an alphabet"""
    return extract_valid_regexes(all_strings(max_length, alphabet))

def regex_apply_all(regex, max_length, alphabet):
    """Returns a generator that takes a compiled regex and yields
    tuples for every string of length from alphabet with whether
    or not it matches the regex"""
    for string in all_strings(max_length, alphabet):
        yield (string, bool(regex.fullmatch(string)))

def triple_count_bound(regex_max_length, string_max_length, alphabet, regex_chars):
    """Returns an upper bound on the size of a dataset generated with the same parameters"""
    count_regexes = sum(len(alphabet + regex_chars) ** length for length in range(regex_max_length + 1))
    count_strings = sum(len(alphabet) ** length for length in range(string_max_length + 1))
    return count_regexes * count_strings


def triple_generator(regex_max_length, string_max_length, alphabet, regex_chars):
    """Returns a generator that gives for every regex-string pair
    up to a length whether or not they match"""
    for regex in all_regexes(regex_max_length, alphabet + regex_chars):
        for string in all_strings(string_max_length, alphabet):
            yield regex.pattern, string, bool(regex.fullmatch(string))

def dataset_generator(regex_max_length, string_max_length, alphabet, regex_chars, random_frac):
    """Returns a generator that gives for every regex-string pair
    up to a length whether or not they match, with strings encoded
    as character index lists"""
    regex_char_int = {c: i + 1 for i, c in enumerate(alphabet + regex_chars)}
    string_char_int = {c: i + 1 for i, c in enumerate(alphabet)}
    
    for regex in all_regexes(regex_max_length, alphabet + regex_chars):
        if len(regex.pattern) != 0:
            regex_ints = [regex_char_int[c] for c in regex.pattern.replace("\\", "")]
            for string in all_strings(string_max_length, alphabet):
                if len(string) != 0 and (random_frac == None or random.random() < random_frac):
                    string_ints = [string_char_int[c] for c in string]
                    yield regex_ints, string_ints, np.int64(int(bool(regex.fullmatch(string))))
