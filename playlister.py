#!/usr/bin/env python3

from sys import argv, stderr
from os import chdir, getcwd
from os.path import isdir, isfile, basename, sep
from glob import iglob
from fnmatch import fnmatch

extensions = ['*.mp3', '*.wma']
initial_path = getcwd()

def findmediafiles(dir):
    """
    Finds the paths to each media file in the directory. The produces
    relative paths relative to the current directory, and sorts them
    too.
    """
    
    def isvalidfile(name):
        """
        Determines if the file is usable in the playlist; it looks
        for specific file extensions, but is crudely case insensitive.
        """
        if isfile(name):
            for pat in extensions:
                if fnmatch(name.lower(), pat):
                    return True
        return False

    allfiles = iglob("**/*", recursive=True)
    validfiles = [fn for fn in allfiles if isvalidfile(fn)]
    validfiles.sort()
    return validfiles


def makeplaylist(dir):
    """
    Creates the playlist for for a directory; if one exists, this function
    will replace it.
    """
    playlist_name = basename(dir.rstrip(sep)) + ".m3u"
    print("Creating " + playlist_name)
            
    chdir(dir)
    
    try:
        with open(playlist_name, "w") as f:
            for filename in findmediafiles(dir):
                f.write(filename)
                f.write('\n')
    finally:
        chdir(initial_path)

# This just processe sthe command line, skipping the first
# entry. That's just the filename of this script.
for dir in argv[1:]:
    if isdir(dir):
        makeplaylist(dir)
    else:
        print("{} is not a directory".format(dir), file=stderr)
