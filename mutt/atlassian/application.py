# -*- coding: utf-8 -*-
'''

@author: Andreas Schiweck

'''

import ConfigParser

from jira import JIRA


def get_jira(config):
    """
    """
    # authenticate
    try:
        username = config.get('auth', 'username')
        password = config.get('auth', 'password')
        basic_auth = username, password
    except ConfigParser.NoOptionError:
        basic_auth = None
    try:
        kerberos = config.get('auth', 'kerberos')
        # config.set('auth', 'kerberos', eval(config.get('auth', 'kerberos')))
        # if kerberos:
        #     return JIRA(config.get('globals', 'url'), kerberos=kerberos)
        #     basic_auth = None
    except ConfigParser.NoOptionError:
        kerberos = False
    return JIRA(config.get('globals', 'url'), basic_auth=basic_auth, kerberos=kerberos)
