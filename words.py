#
# logic for dealing with words
#
from random import randint


def get_country():
    countries = read_countries()
    rand = randint(0, len(countries) - 1)
    country = countries[rand]
    return country.strip()


def read_countries():
    with open('countries.txt') as f:
        countries = f.readlines()
        return countries


def remove_letter(letters, letter):
    le = letter.upper()
    i = ord(le) - 65
    letters[i] = "_"


def updated_blank_word(word, blank_word, letter):
    """ Add letters to the blank word if needed. """
    new_word = ''
    for i in range(len(word)):
        if word[i].upper() == letter:
            new_word += word[i]
        else:
            new_word += blank_word[i]
    return new_word


def get_words_within_x_chars(words, x=23):
    """ :param words: list of words
    :param x: max number of chars per line
    :return: number of words returned, the new phrase """
    new_word = ''
    word_count = 0
    for word in words:
        if len(new_word + ' ' + word) < x:
            new_word = new_word + ' ' + word
            word_count += 1
        else:
            break
    return word_count, new_word


def format_blank_word(blank_word):
    """ our country name might be very large, so want
     to break it down a bit, 23 chars or less per line """
    words = blank_word.split(' ')
    words_len = len(words)
    new_words = []
    used_words = 0
    while used_words != words_len:
        word_count, new_word = get_words_within_x_chars(words[used_words:])
        new_words.append(new_word)
        used_words += word_count
    return new_words


def make_word_blank(word):
    blank_word = ''
    for ch in word:
        if ch == ' ':
            blank_word += ' '
        else:
            blank_word += '_'
    return blank_word
