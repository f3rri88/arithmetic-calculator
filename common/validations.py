import os.path
import re


def is_filepath(filepath):
    '''Returns True if the filepath is valid, False if not.'''
    return re.match(r'^(.*/)?(?:$|(.+?)(?:(\.[^.]*$)|$))', filepath) \
        and os.path.isfile(filepath)
