#!/usr/bin/env python3

from sys import argv
from os import chdir, getcwd
from os.path import isdir, isfile, basename, sep
from glob import iglob
from fnmatch import fnmatch

extensions = ['*.mp3', '*.wma']

def isvalidfile(name):
    if isfile(name):
        for pat in extensions:
            if fnmatch(name.lower(), pat):
                return True
    return False

for dir in argv[1:]:
    dir = dir.rstrip(sep)
    initial_path = getcwd()
    if isdir(dir) and not dir.startswith('.'):
        playlist_name = basename(dir) + ".m3u"
        print(playlist_name)
                
        chdir(dir)
        
        with open(playlist_name, "w") as f:
            for filename in iglob("**/*", recursive=True):
                if isvalidfile(filename):
                    f.write(filename + '\n')

        chdir(initial_path)

