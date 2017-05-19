# -*- coding: utf-8 -*-
'''

@author: Andreas Schiweck

'''

import ConfigParser
import os
import re
import sys


HOME = os.path.expanduser('~')
CONFIG = os.path.join(HOME, '.mutt-atlassian.ini')
ISSUEKEY = re.compile('(\w+-\d+)')
TERMWIDTH = 80


def create_configfile(path):
    """
    """
    config = ConfigParser.RawConfigParser()
    config.add_section('globals')
    config.set('globals', 'url', 'https://jira.atlassian.com')
    config.set('globals', 'version', 1)
    config.set('globals', 'clear', True)
    config.add_section('auth')
    config.set('auth', '# username', '<USERNAME>')
    config.set('auth', '# password', '<PASSWORD>')
    config.set('auth', 'kerberos', False)
    config.add_section('mutt2jira')
    config.set('mutt2jira', 'assign', True)
    with open(path, 'wb') as configfile:
        config.write(configfile)


def get_config(path):
    """
    """
    # generate config file if missing
    try:
        f = open(path, 'r')
        f.close()
    except IOError:
        print "Created missing config file %s, please review!" % path
        create_configfile(path)
        sys.exit(1)
    # read config file
    config = ConfigParser.RawConfigParser()
    config.read(path)
    try:
        config.set('mutt2jira', 'assign', eval(config.get('mutt2jira', 'assign')))
    except ConfigParser.NoOptionError:
        config.set('mutt2jira', 'assign', False)
    try:
        config.set('globals', 'clear', eval(config.get('globals', 'clear')))
    except ConfigParser.NoOptionError:
        config.set('globals', 'clear', False)
    try:
        config.set('auth', 'kerberos', eval(config.get('auth', 'kerberos')))
    except ConfigParser.NoOptionError:
        config.set('auth', 'kerberos', False)
    return config
