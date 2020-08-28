#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
import requests
import lxml.html
import re

def get_entry(word):
    '''
    Return entry or None if there is no entry for the given word.
    The function scraps the "https://sjp.pwn.pl" website to find the entry.
    '''
    url = 'https://sjp.pwn.pl/szukaj/'
    page = requests.get(url + word + '.html')
    tree = lxml.html.fromstring(page.content)

    entry_titles_xpath = ('//div[@class="entry "]/div[@class="entry-body"]'
        '/div/span[@class="tytul"]/a/text()')
    entry_titles = tree.xpath(entry_titles_xpath)
    entry_titles = list(set(entry_titles)) # Eliminate duplicates

    entry_defs_xpath = '//div[@class="znacz"]/text()'
    entry_defs = tree.xpath(entry_defs_xpath)
    # Remove '«' and '»' chars, and '\n' elements
    entry_defs = [re.sub('[«»]', '', e) for e in entry_defs if e != '\n']

    # Check if there is an entry for the given word
    if entry_titles == [] or entry_defs == []:
        return None

    return entry_titles, entry_defs

def print_entry(entry_titles, entry_defs):
    titles = ', '.join(entry_titles)

    # Number definitions and separate them by newlines, resulting in a string
    defs = [str(i+1) + '. ' + entry_defs[i] for i in range(len(entry_defs))]
    defs = '\n'.join(defs)

    print(titles, '\n', defs, sep='')

def print_help():
    print('Usage:', sys.argv[0], '[-h|--help] <word_to_define>...')

def main():
    if len(sys.argv) >= 2:
        if '-h' in sys.argv or '--help' in sys.argv:
            print_help()
        else:
            # A flag to indicate whether we are printing the first entry
            first_flag = True

            for arg in sys.argv[1:]:
                entry = get_entry(arg)
                if entry != None:
                    # If this is not the first entry, print a precending
                    # newline to separate entries
                    if first_flag != True: print() 

                    print_entry(*entry)

                    if first_flag == True: first_flag = False
    else:
        print(sys.argv[0], ': too few arguments', sep='', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
