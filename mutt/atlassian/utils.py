# -*- coding: utf-8 -*-
'''

@author: Andreas Schiweck

'''

import textwrap

from mutt.atlassian.config import TERMWIDTH

def _compact(string, length=0):
    """
    """
    if length > 0 and len(string) > length:
        out = []
        words = string.split()
        suffix = ' [...]'
        l, index = len(suffix), 0
        while l <= length: # - len(suffix):
            out.append(words[index])
            l += len(words[index]) + 1
            index += 1
        string = ' '.join(out[:-1]) + suffix
    return textwrap.fill(string, width=TERMWIDTH, replace_whitespace=True)


def get_yes_or_no(question):
    """
    """
    reply = str(raw_input('\n'+question+'\n(<y>/n)> ')).lower().strip()
    if not reply or reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return get_yes_or_no(question)
