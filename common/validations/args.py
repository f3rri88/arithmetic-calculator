import os.path
import re


def is_filepath(filepath):
    '''Returns True if the filepath is valid, False if not.'''
    re.match(r'^(.*/)?(?:$|(.+?)(?:(\.[^.]*$)|$))', filepath)
    os.path.isfile(filepath)
