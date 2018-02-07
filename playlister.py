#!/usr/bin/env python3

from sys import argv, stderr
from os import chdir, getcwd
from os.path import isdir, isfile, basename, sep
from glob import iglob
from fnmatch import fnmatch

initial_path = getcwd()

def split_digits(text):
    buffer=[]
    for c in text:
        if len(buffer) == 0:
            buffer.append(c)
        elif buffer[-1][-1].isdigit() == c.isdigit():
            buffer[-1]+=c
        else:
            buffer.append(c)
    return buffer
    
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
        
    max_number_len = max((len(part)
        for file in files 
        for part in split_digits(file)
        if part[0].isdigit()))
    
    def pad_numbers(file):
        parts = (
            part.rjust(max_number_len, "0")
            if part[0].isdigit() else part
            for part in split_digits(file))
        return "".join(parts)
        
    return sorted(files, key=pad_numbers)

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

# This just processe sthe command line, skipping the first
# entry. That's just the filename of this script.

if len(argv) < 2:
    print("Usage: playlister.py DIR1 DIR2 ...")
else:
    for dir in argv[1:]:
        if isdir(dir):
            make_playlist(dir)
        else:
            print("{} is not a directory".format(dir), file=stderr)
