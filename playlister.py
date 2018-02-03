#!/usr/bin/env python3

from sys import argv, stderr
from os import chdir, getcwd
from os.path import isdir, isfile, basename, sep
from glob import iglob
from fnmatch import fnmatch

extensions = ['*.mp3', '*.wma']
initial_path = getcwd()

def find_media_files(dir):
    """
    Finds the paths to each media file in the directory. The produces
    relative paths relative to the current directory, and sorts them
    too.
    """
    
    def is_valid_file(name):
        """
        Determines if the file is usable in the playlist; it looks
        for specific file extensions, but is crudely case insensitive.
        """
        if isfile(name):
            for pat in extensions:
                if fnmatch(name.lower(), pat):
                    return True
        return False
    
    all_files = iglob("**/*.*", recursive=True)
    valid_files = [fn for fn in all_files if is_valid_file(fn)]
    valid_files.sort()
    return valid_files


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
                f.write('\n')
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
