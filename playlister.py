#!/usr/bin/env python3

from sys import argv, stderr
from os import chdir, getcwd
from os.path import isdir, isfile, basename, sep
from glob import iglob
from fnmatch import fnmatch

initial_path = getcwd()

def sorted_smartly(to_sort):
    """
    Sorts the given list of strings alphabetically, but with
    extra smarts to handle simple numbers. It effectly sorts
    them as if they with 0 padded so all numbers are the same
    length; this makes them sort numerically.
    """
    def split_digits(text):
        """
        Splits a string into segments that cover every character; Digits
        are placed in separate segments from everything else.
        """
        buffer=[]
        for c in text:
            if len(buffer) == 0:
                buffer.append(c)
            elif buffer[-1][-1].isdigit() == c.isdigit():
                buffer[-1]+=c
            else:
                buffer.append(c)
        return buffer

    # This is how long we will make all the digits.
    max_number_len = max((len(part)
        for file in to_sort
        for part in split_digits(file)
        if part[0].isdigit()))
    
    def pad_numbers(text):
        """
        This breaks down the string given and padds any numbers
        found, then reassambles it all.
        """
        parts = (
            part.rjust(max_number_len, "0")
            if part[0].isdigit() else part
            for part in split_digits(text))
        return "".join(parts)
        
    return sorted(to_sort, key=pad_numbers)
    
def find_media_files(dir, extensions = ["mp3", "wma"]):
    """
    Finds the paths to each media file in the directory. The produces
    relative paths, relative to the current directory, and sorts them
    too. Only files with the extensions given are returend.
    """
    
    def make_pattern(ext):
        """
        Creates the glob pattern for a particular extension; it
        matches the file extension case insensitively, even on
        Linux.
        """
        def insensitive(ch):
            """
            If 'ch' is a letter, returns a pattern that matches it
            in either case. If not, returns it unchanged.
            """
            if ch.isalpha():
                return "[{}{}]".format(ch.lower(), ch.upper())
            else:
                return ch

        return "**/*." + "".join((insensitive(c) for c in ext))
    
    # use a set in case a file matches two patterns; we want each file
    # once only.
    
    files = set()
    
    for ext in extensions:
        for fn in iglob(make_pattern(ext), recursive=True):
            files.add(fn)
        
    return sorted_smartly(files)

def make_playlist(dir):
    """
    Creates the playlist for for a directory; if one exists, this function
    will replace it.
    """
    playlist_name = basename(dir.rstrip(sep)) + ".m3u"
    print("Creating " + playlist_name)
     
    # change current director so that find_media_files produces
    # paths relative to 'dir'
        
    chdir(dir)
    
    try:
        with open(playlist_name, "w") as f:
            for filename in find_media_files(dir):
                f.write(filename)
                f.write("\n")
    finally:
        chdir(initial_path)

# This just processes the command line, skipping the first
# entry. That's just the filename of this script anyway.

if len(argv) < 2:
    print("Usage: playlister.py DIR1 DIR2 ...")
else:
    for dir in argv[1:]:
        if isdir(dir):
            make_playlist(dir)
        else:
            print("{} is not a directory".format(dir), file=stderr)
