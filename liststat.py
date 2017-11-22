#!/usr/bin/env python3

'''
NOTE:   You can customize the results of this script by choosing the character sets or
        word positions (first, second, last, etc.) in which you are most interested.

        Character sets are represented by integers for easy binary comparison.
        This really cuts down on the 'if' statements. (see 'charsets' variable)

        This script is designed based on the concept of a "simple mask", which is a
        password broken into "chunks" based on character type. (word, number, etc.)
        E.g., "Password123!" would be broken into 4 parts: "P", "assword", "123", "!"
        chunks can be further generalized by merging character sets.
        For example, merging upper and lower alpha would yield: "Password", "123", "!"

TODO:
For heaven's sake rewrite ListStat._count_chunks

with ListStat:      20s
without ListStat:   7s
1. move as much as possible to ListStat
2. multiprocess ListStat
3. merge ListStats into one
4. report
'''

import os
import pickle
import string
import argparse
from time import sleep
from threading import Lock
from sys import argv, exit, stdin, stderr
#from signal import signal, SIGPIPE, SIG_DFL

#signal(SIGPIPE,SIG_DFL) # don't ignore SIGPIPE (prevents broken pipe error)



### DEFAULTS - FEEL FREE TO MODIFY, CAREFULLY ###


# characters to look for when parsing 1337 words
leet_specials   = ('@', '$')                        # leet words can start or end with special characters
leet_numbers    = ('8', '3', '1', '0', '5', '7')    # leet numbers are not included on the beginning or end of words
                                                    # for example, "$@ssy1" would be split into "$@ssy" and "1"


'''
chunks to count:

--> Useful for finding common words, appended/prepended numbers, punctuation, etc.

Determines how individual parts of words are added to stats (see help(Mask.add) for explanation)

    1.  'chunk' references a position in the word.
        In the word 'pass@123', chunk 0 is 'pass', 1 is '@', and 2 (or -1) is '123', etc.

    2.  'char_types' determines which character types to include.  (see "charsets" object below)
        If 'char_types' is '(1, 8)', only numeric and special chunks will be gathered.  Must be a tuple.

    3.  'ignore_placement' determines how results are collected and displayed.
        If it is True, placement is ignored and all positions are counted
        E.g., '123' in 'pass123' and '123pass' would both be counted if char_type was 1

    'chunk'     'char_types'
'''
chunks_to_count = {
    #   { -1: (1, 8, 6) } would match numbers, special characters, and mixed-alpha
    #   words in position -1 (the last part of the word)
    #   (note: mixed-alpha would match either lowercase, uppercase, or both)

    # index         # chartype
    0:              (6,),
    -1:             (1, 8)

}

chunks_leet         = True # consider leet characters when analyzing chunks
ignore_placement    = True # ignores chunk's placement in word (see above)
include_count       = True # includes number of occurrences when writing stats to file

word_requirements = [
    # each entry is a function which takes a WordStat() object,
    # and evaluates to either True or False
    # use this if you want to have precise control over which words get analyzed

    #                                                                                       # EACH WORD MUST:
    # lambda x: [i[0] & 6 > 0 for i in x.mask.generalize(6, leet=True)].count(True) == 2,   # include exactly 2 words
    lambda x: [i[0] & 6 > 0 for i in x.mask.generalize(6, leet=True)].count(True) < 3,      # include less than 3 words
    # lambda x: [i[0] for i in x.mask.lst].count(1) >= 2                                    # include 2 or more number chunks
]

wordlist_encoding = 'utf-8' # don't change unless you get errors



### INIT CODE - DO NOT TOUCH ###


# merges chunks_to_count if placement is being ignored
if ignore_placement:

    _s = set()

    for s in chunks_to_count.values():
        _s = _s.union(s)

    chunks_to_count = {}
    chunks_to_count['all'] = tuple(_s)


'''
Data object for referencing character types, masks, etc.
Indexed in binary, to allow use of AND and OR operators when checking charsets.
Used throughout the script.

char_type   friendly_name               mask        more_friendly_name          short_name
'''
charsets = {

    1:      ('numeric',                 '?d',       'number',                   'd'),
    2:      ('loweralpha',              '?l',       "word",                     'w'),
    4:      ('upperalpha',              '?u',       "word",                     'w'),
    8:      ('special',                 '?s',       "special",                  's'),
    3:      ('loweralphanum',           None,       'word',                     'w'),
    5:      ('upperalphanum',           None,       'word',                     'w'),
    6:      ('mixedalpha',              None,       'word',                     'w'),
    7:      ('mixedalphanum',           None,       'word',                     'w'),
    9:      ('specialnum',              None,       'specialnum',               'w'),
    10:     ('loweralphaspecial',       None,       'word',                     'w'),
    11:     ('loweralphaspecialnum',    None,       'word',                     'w'),
    12:     ('upperalphaspecial',       None,       'word',                     'w'),
    13:     ('upperalphaspecialnum',    None,       'word',                     'w'),
    14:     ('mixedalphaspecial',       None,       'word',                     'w'),
    15:     ('all',                     None,       'word',                     'w'),
}

# single character types (not mixed)
chartypes = (1, 2, 4, 8)

total_processed = 0
total_skipped = 0



### CLASSES ###


class ListStat:
    '''
    stores:     global information on wordlist
    '''

    def __init__(self, ignore_leet=False):
	
        self.ignore_leet    = ignore_leet

        # list stats
        self.total          = 0  # total number of words
        self.skipped        = 0  # total words skipped (determined beforehand)
        self.charset        = 0  # collective character set for list
        self.char_total     = 0  # total number of characters
        self.chunk_total    = {} # dictionary for individual chunk totals

        # word stats
        self.lengths        = {}
        self.charsets       = {}
        self.simple_masks   = {}
        self.masks          = {}
        self.chunks         = {}
        self.chars          = {}

        # nested dictionary in which to store interesting chunks
        # format is { position: { char_type: { 'chunk': [count, recurrance] } } }
        # 'position' is 'all' if it is being ignored
        # 'recurrance' is the number of times this chunk's charset has been found more than once in the same word
        for position in chunks_to_count:
            self.chunks[position] = {}
            self.chunk_total[position] = {}
            for charset in chunks_to_count[position]:
                self.chunks[position][charset] = {}
                self.chunk_total[position][charset] = 0



    def update(self, word):

        # globals
        self.total += 1
        self.charset = self.charset | word.charset

        # specifics
        self._add_count(self.lengths, word.length)
        self._add_count(self.charsets, word.charset)
        self._add_count(self.masks, str(word.mask))
        self._count_chunks(word.mask)
        self._count_chars(word.mask)

        # simple mask - moved from WordStat for efficiency
        # arg '6' means that upper and lower case are grouped together
        _simple_mask = word.mask.generalize(charset=6, leet=(not self.ignore_leet))
        simple_mask = ''
        for s in _simple_mask:
            simple_mask += charsets[s[0]][3]

        self._add_count(self.simple_masks, simple_mask)



    def report(self, max_results=25, _print=True):
        '''
        returns:    contents of ListStat() object
                    format is: 
        does:       can also write results to screen or file
        '''

        # set up report data
        
        #   dictionary          friendly_name       total_processed         total_unique                print_key                           file_key

        self.to_report = [
            (self.lengths,      "word lengths",     self.total,             len(self.lengths),          None,                               None),
            (self.charsets,     "character sets",   self.total,             len(self.charsets),         lambda x: charsets[x][0],           lambda x: charsets[x][0]),
            (self.simple_masks, "simple masks",     self.total,             len(self.simple_masks),     self._simple_mask_print,            None),
            (self.masks,        'masks',            self.total,             len(self.masks),            None,                               None),
            (self.chars,        'characters',       self.char_total,        len(self.chars),            None,                               None)
        ]

        for position in chunks_to_count:
            for charset in chunks_to_count[position]:
                self.to_report.append( (self.chunks[position][charset], "chunks ({}, position {})".format(charsets[charset][0], \
                    str(position)), self.chunk_total[position][charset], len(self.chunks[position][charset]), None, None) )

        if _print:

            try:
                print("\n\n WORDLIST STATISTICS")
                print(" ===================\n")
                print(" Total Words:    {:,} processed / {:,} skipped".format(self.total, self.skipped))
                print(" Character Set:  {}\n".format(str(charsets[self.charset][0])))

            except KeyError:
                error_print("No words for report")
                exit(1)

            for _stat in self.to_report:
                sorted_list = self._sort_stat(_stat[0], max_results=max_results)

                #    _console_print(self, sorted_list, fname, ttl, total_unique, key=None, max_results=25):
                self._console_print(sorted_list, _stat[1], _stat[2], _stat[3], key=_stat[4], max_results=max_results)



    def write(self, out_dir, include_count=False):

        self.report(_print=False)

        for _stat in self.to_report:

            sorted_list = self._sort_stat(_stat[0])

            key = _stat[5]

            if key is None:
                key = lambda x: str(x)          

            filename = '{}.txt'.format(os.path.join(out_dir, _stat[1]))

            with open(filename, 'w', encoding='utf-8') as f:

                for i, count, recurrance in sorted_list:
                    i = key(i)
                    if include_count:
                        f.write('{},{:d},{:d}\n'.format(i, count, recurrance))
                    else:
                        f.write('{}\n'.format(i))



    def trim(self, dct, percentage, ttl, max_results=None, key=lambda x: x[1] + x[2]):
        '''
        given a percentage, yields entries from list, truncated
        to produce desired percentage of coverage
        '''

        l = self._sort_stat(dct, max_results=max_results, key=key) # sorted list

        if percentage == 100:
            for i in l:
                yield i[0]
        else:
            p = ttl * ((percentage % 100) / 100)

            a = 0 # sum of entry totals
            c = 0 # number of entries

            for entry in l:
                if a > p: break
                if max_results:
                    if c >= max_results: break

                c += 0
                a += entry[1]
                yield entry[0]



    def _sort_stat(self, dct, key=lambda x: x[1], max_results=None):

        sorted_list = []

        for k in dct:

            sorted_list.append( (k, dct[k][0], dct[k][1]) )

        sorted_list.sort(key=key, reverse=True)
        if max_results:
            return sorted_list[:max_results]
        else:
            return sorted_list



    def _console_print(self, sorted_list, fname, ttl, total_unique, key=None, max_results=25):

        if ttl <= 0:
            return

        try:

            if key is None:
                key = lambda x: str(x)

            print("\n Top {:d} {}:   (out of {:d})".format(max_results, fname, total_unique))

            _max = max(sorted_list, key=lambda x: len(key(x[0])))
            col_width = len(key(_max[0]))

            if col_width < 10:
                col_width = 10

            for i, count, recurrance in sorted_list:
                i = key(i)
                print("   {: >{}}:  {:.1f}%  ({:d})".format(i, col_width, ((count / ttl) * 100), count))
            print()

        except ValueError:
            print("   None")



    def _count_chunks(self, mask):
        '''
        Stores statistics for common password chunks
        '''

        for position in chunks_to_count:

            for charset in chunks_to_count[position]:

                temp_lst = mask.generalize(charset, leet=(self.ignore_leet))

                # recurrance = True if more than 1 chunk with the same
                # charset appears in one word
                recurrance = False
                if [e[0] | charset == charset for e in temp_lst].count(True) >= 2:
                    recurrance = True

                m_length = len(temp_lst) # how many chunks the word has
                counted_chunks = []

                # create iterable storing which parts of word to count
                if ignore_placement:
                    l = range(m_length)
                else:
                    l = chunks_to_count.keys()

                # for place in list
                for p in l:

                    # convert negative indices to positive to avoid counting twice
                    if p < 0:
                        p = m_length + p

                    try:
                        # charset, chunk
                        c, h = temp_lst[p]

                    except IndexError:
                        continue

                    # only count once per word
                    if p in counted_chunks:
                        continue

                    if c & charset > 0:
                        self._add_count(self.chunks[position][charset], h, recurrance=recurrance)
                        self.chunk_total[position][charset] += 1
                        counted_chunks.append(p)




    def _simple_mask_print(self, _simple_mask):

        simple_mask = []
        for s in _simple_mask:
            if s == 'w':
                simple_mask.append('word')
            elif s == 'd':
                simple_mask.append('number')
            else:
                simple_mask.append('special')

        return '-'.join(simple_mask)




    def _add_count(self, dct, obj, recurrance=False):
        '''
        add obj to dct, incrementing its count if it already exists
        increment ttl (total) if requested
        recurrance is a separate counter for chunks whose charset occurs more than once in the word
        '''

        try:
            dct[obj][0] += 1
        except KeyError:
            dct[obj] = [1,0]

        if recurrance:
            dct[obj][1] += 1



    def _count_chars(self, mask):

        for s in mask.lst:
            for c in s[1]:
                self._add_count(self.chars, c)
                self.char_total += 1




class WordStat:
    '''
    stores basic info about each word
    '''

    def __init__(self, word, parse=True):

        self.string = word

        self.parsed = False
        if parse:
            self.parse()


    def parse(self):

        if self.parsed:
            return

        self.charset = 0
        self.length = 0
        self.mask = Mask()

        for letter in self.string:
            self.length += 1

            self._nibble(letter)

        self.parsed = True
        del self.string # string is parsed, so we're done with it


    def __repr__(self):

        self.parse()

        pretty = ''
        
        for group in self.mask.lst:
            pretty += group[1]

        return pretty


    def _nibble(self, letter):

        # character sets

        if letter.islower():
            chartype = 2
        elif letter.isupper():
            chartype = 4
        elif letter.isdecimal():
            chartype = 1
        else:
            chartype = 8

        self.charset = self.charset | chartype

        self.mask.add(letter, chartype)





class Mask:

    def __init__(self):

        # representation of mask, split by character type
        # format is [ [char_type, 'word_chunk'], ... ]
        self.lst = []

        # stores 'generalized' masks - True = leet, False = normal
        self.lst_generalized = {True: {}, False: {}}



    def __repr__(self):

        pretty = ''

        for group in self.lst:
            pretty += (charsets[group[0]][1] * len(group[1]))

        return pretty



    def add(self, letter, chartype):
        '''
        if the current chunk matches the character type, add to it
        else, make a new one
        '''

        try:
            if self.lst[-1][0] == chartype:
                self.lst[-1][1] += letter
            else:
                raise IndexError

        except IndexError:
            self.lst.append( [chartype, letter] )



    def generalize(self, charset=6, leet=False):
        '''
        Groups chunks together if they are both enveloped by desired charset
        e.g. [ [2, 'asdf'], [4, 'ASDF'] ] --> [ [6, 'asdfASDF' ] ]
        '''

        # don't modify if charset is numeric or special, or if there's only one chunk
        if len(self.lst) < 2 or charset == 1 or charset == 8:
            return self.lst

        try:
            return self.lst_generalized[leet][charset]

        except KeyError:

            if leet:
                l = self._leet(charset)
                self.lst_generalized[leet][charset] = l
                return l

            # take the first chunk and add it, making sure to change charset if necessary
            c, s = self.lst[0]
            if c | charset == charset:
                c = charset

            temp_lst = [ [c, s] ]

            for c2, s2 in self.lst[1:]: # chartype, chunk/string

                c1, s1 = temp_lst[-1]

                if c2 | charset == charset:
                    c2 = charset

                if c1 == c2:
                    temp_lst[-1][1] += s2
                else:
                    temp_lst.append( [c2, s2] )

            self.lst_generalized[leet][charset] = temp_lst
            return temp_lst


    def _leet(self, charset=6):
        '''
        Groups chunks together, including "leet" characters.
        E.g., ('P', 'a' '@' 's' '5' 'word') --> ('P@s5word') 
        Does not include leet numbers at the beginning or end of words.
        '''

        num_chunks = len(self.lst)
        num_range = range(num_chunks)
        leet_lst = []
        _start, _end = False, False

        num_chunks -= 1

        for n in num_range:

            # if this chunk includes desired charset, or leet specials
            if ( (self.lst[n][0] | charset) == charset ) or ( all(c in leet_specials for c in self.lst[n][1]) ):
                if not _start:
                    start, _start = n, True
                else:
                    end, _end = n, True
                if n < num_chunks:
                    continue

            # if this chunk is only 'leet' numbers
            elif all(c in leet_numbers for c in self.lst[n][1]):
                if n < num_chunks:
                    continue

            if _start and _end:
                leet_lst.append((start, end))

            _start, _end = False, False

        temp_lst = []
        i = 0

        # need to loop twice, since analysis isn't complete
        # until first iteration is finished
        for n in num_range:
            try:
                start, end = leet_lst[i]
            except IndexError:
                start, end = -1, -1

            if n < start or n > end:
                temp_lst.append(self.lst[n])

            elif n == start:
                c2, s2 = self.lst[start]
                for c1, s1 in self.lst[start+1:end + 1]:
                    c2 = c2 | c1
                    s2 = s2 + s1
                temp_lst.append([c2, s2])

            elif n == end:
                i += 1

            else:
                continue

        self.lst_generalized[True][charset] = temp_lst 
        return temp_lst





### FUNCTIONS ###

def filter_wordlist(wordlist, excl_charset=None, min_charset=None, min_chartypes=None, \
        max_chartypes=None, clean_word=False, other=word_requirements):
    '''
    takes:      wordlist iterable
    does:       checks words against requirements
    yields:     matching Word() objects
    '''
    global total_processed
    global total_skipped

    bits = [1,2,4,8,16,32,64,128]

    for w in wordlist:

        try:

            word = WordStat(w)

            if excl_charset:
                assert not word.charset & excl_charset == excl_charset
            if min_charset:
                assert word.charset & min_charset == min_charset

            #chartype_count = [word.charset & b > 0 for b in bits].count(True)  # .995 usec per loop
            chartype_count = bin(word.charset).count('1')                       # .29 usec per loop

            if min_chartypes:
                assert chartype_count >= min_chartypes
            if max_chartypes:
                assert chartype_count <= max_chartypes
            if clean_word:
                assert len(word.mask.lst) < 10
            if other:
                assert all(r(word) for r in other)

            total_processed += 1
            yield word

        except AssertionError:
            total_skipped += 1
            continue



def read_input(infile, minlength=1, maxlength=100):
    '''
    takes:      file-type object
    does:       decodes, checks line length
    yields:     individual lines
    '''

    global total_skipped

    while 1:

        line = infile.readline()

        try:

            if type(line) == bytes:
                line = line.decode(encoding=wordlist_encoding)

            if not line:
                break

            line = line.strip('\r\n')
            length = len(line)
            assert ( length >= minlength ) and ( length <= maxlength )
            yield line

        except (UnicodeDecodeError, AssertionError):
            total_skipped += 1
            continue



def error_print(a):
    stderr.write('\n[!] {}\n'.format(str(a)))



def _check_dir(d):
    try:
        os.makedirs(d)
        assert os.path.isdir(d), "Can't create output directory"
    except OSError:
        pass




if __name__ == '__main__':

    ### SET UP ARGUMENTS ###

    # set up string for help
    charset_help = 'Character sets:\n\n'
    for k in charsets:
        charset_help += '{}:\t{}\n'.format(str(k), charsets[k][0])


    # allows newlines in help output
    class SmartFormatter(argparse.HelpFormatter):

        def _split_lines(self, text, width):
            if text.startswith('| '):
                return text[2:].splitlines()
            return argparse.HelpFormatter._split_lines(self, text, width)


    # overridden if 'progress' option is enabled
    def _print_progress(*a):
        return


    parser = argparse.ArgumentParser(description='Generate statistics on a wordlist.', formatter_class=SmartFormatter)
    parser.add_argument('input_file',   nargs='?',  type=argparse.FileType(mode='rb'),  default=stdin.buffer,       help="List to be analyzed; leave blank for STDIN")
    parser.add_argument('-s', '--save',             type=os.path.abspath,               default=None,               help="Save stats to this file", metavar='FILE')
    parser.add_argument('-l', '--load',             type=os.path.abspath,               default=None,               help="Load previous stats from this file", metavar='FILE')
    parser.add_argument('-w', '--write',            type=os.path.abspath,               default=None,               help="Save stats as individual wordlists", metavar='FILE')
    parser.add_argument('--include-count',          action='store_true',                                            help="Include number of occurrences in output")
    parser.add_argument('--no-leet',                action='store_true',                default=not chunks_leet,    help="Don't treat 1337 characters specially")
    parser.add_argument('-m', '--min-length',       type=int,                           default=1,                  help="Minimum word length", metavar='')
    parser.add_argument('-M', '--max-length',       type=int,                           default=100,                help="Maximum word length", metavar='')
    parser.add_argument('-p', '--no-progress',      action='store_true',                                            help="Don't display progress")
    parser.add_argument('-c', '--clean',            action='store_true',                                            help="Skip extremely complex passwords")
    parser.add_argument('--max-results',            type=int,                           default=25,                 help="Only print this many results for each stat", metavar='INT')
    parser.add_argument('--min-chartypes',          type=int,                           default=None,               help="Words must have at least this many character types", metavar='INT')
    parser.add_argument('--max-chartypes',          type=int,                           default=None,               help="Words must have at most this many character types", metavar='INT')
    parser.add_argument('-E', '--exclude',          type=int,                           default=None,               help="Words cannot have this character set", metavar='')
    parser.add_argument('-R', '--require',          type=int,                           default=None,               help="| Words must have at least this character set\n\n{}".format(charset_help), metavar='')


    try:

        rc = 1

        ### PARSE ARGUMENTS ###

        # print help if no arguments and no pipe to stdin
        if stdin.isatty() and len(argv) < 2:
            parser.print_help()
            exit(2)

        options = parser.parse_args()

        # print progress
        if not options.no_progress:
            def _print_progress(word=''):
                stderr.write('  {:,} processed / {:,} skipped   ({})                 \r'.format(total_processed, total_skipped, word))

        # check that output dir exists
        if options.write:
            _check_dir(options.write)
        if options.save:
            _check_dir(os.path.dirname(options.save))
            assert not os.path.exists(options.save)
            


        ### START MAIN SCRIPT ###

        if options.load:

            assert os.path.isfile(options.load), "Can't find file to load"

            with open(options.load, 'rb') as in_file:
                list_stats = pickle.load(in_file)

        else:

            word_gen =  filter_wordlist(read_input(options.input_file, options.min_length, options.max_length), \
                        options.exclude, options.require, options.min_chartypes, options.max_chartypes, options.clean)

            list_stats = ListStat(options.no_leet)

            c = 1
            for word in word_gen:
                if c % 1000 == 0:
                    _print_progress(word)
                c += 1
                list_stats.update(word)


        rc = 0

    except argparse.ArgumentError:
        error_print("Check your syntax. Use -h for help.")
        rc = 2
    except AssertionError as e:
        error_print(e)
        rc = 2
    except KeyboardInterrupt:
        error_print("Program interrupted.")
        rc = 1
    finally:
        try:
            list_stats.skipped = total_skipped

            if options.save:
                with open(options.save, 'wb') as out_file:
                    pickle.dump(list_stats, out_file)

            if options.write:
                list_stats.write(options.write)

            list_stats.report(options.max_results)
        except NameError:
            exit(2)
        exit(rc)