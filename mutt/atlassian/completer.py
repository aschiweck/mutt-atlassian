# -*- coding: utf-8 -*-
'''

@author: Andreas Schiweck

'''

import re
import readline

# import logging
# LOG_FILENAME = '/tmp/completer.log'
# logging.basicConfig(
#     filename=LOG_FILENAME,
#     level=logging.DEBUG,
# )


class JIRACompleter(object):


    def __init__(self, options):
        # self.options = sorted(options)
        self.options = options
        # we provide the completer
        readline.set_completer(self.completer)
        # tab as complete
        readline.parse_and_bind("tab: complete")
        # whole line completition without any delimiters
        readline.set_completer_delims('')
        # an optional method for dynamic options updates
        self.updater = None
        # keep track of last used completion text
        self.text = None


    def completer(self, text, state):

        # always complete the whole buffer
        text = readline.get_line_buffer()

        if text != self.text:
            self.text = text
            self.update()

        # response = [ self.options[key] for key in self.options.keys() if self.options[key].startswith(text) ]

        words = text.split()
        # logging.debug('words=%s', words)
        response = []
        for v in self.options.keys():
            value = self.options[v]
            match = True
            for word in words:
                word = word.replace('.', '\.')
                word = word.replace('(', '\(')
                word = word.replace(')', '\)')
                if not re.search(word, value, re.I):
                    match = False
                    break
            if match:
                response.append(value)

        try:
            # logging.debug('response=%s', response)
            # logging.debug('return=%s, state=%s', response[state], state)
            return response[state]
        except IndexError:
            # logging.debug('INDEXERROR=%s' % state)
            return None

        # Abbruch bei UTF-8 Antworten: uni ser -> Abbruch bei Köln
        # Korrektur von line buffer bei gemeinsamem anfang: cwx -> c
        # Abbruch bei UTF-8 Antworten und Completition auf restlichem Ergebnis: uni -> unibonn.
        # Korrektur von line buffer bei gemeinsamem anfang: catw intern -> catWorkX Intern


    def update(self):
        # logging.debug('needs update')
        if self.updater:
            # logging.debug('calling updater')
            self.options = self.updater(self.text)
