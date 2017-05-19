import pytest

import os
import re

from ConfigParser import NoOptionError

from mutt.atlassian.config import get_config
from mutt.atlassian.config import create_configfile
# from mutt.atlassian.config import CONFIG
# from mutt.atlassian.config import ISSUEKEY
# from mutt.atlassian.application import get_jira


class TestConfig:

    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        self.tmpdir = tmpdir.strpath
        self.configfile = os.path.join(self.tmpdir, '.mutt-atlassian.ini')
        create_configfile(self.configfile)


    # def test_get_jira(self):
    #     jira = get_jira(get_config(self.configfile))


    # def test_ISSUEKEY(self):
    #     KEYS = ('ABC-123 Lorem ipsum', 'Lorem ABC-123 ispum')
    #     for key in KEYS:
    #         assert re.search(ISSUEKEY, key)
    #     KEYS = ('ABC123 Lorem ipsum', 'Lorem ABC123 ipsum')
    #     for key in KEYS:
    #         assert not re.search(ISSUEKEY, key)


    # def test_create_configfile(self, tmpdir):
    #     assert os.path.isfile(self.configfile)


    # def test_get_config(self):
    #     config = get_config(self.configfile)
    #     assert config.get('globals', 'clear')
    #     assert config.get('globals', 'version') == '1'
    #     assert config.get('globals', 'url') == 'https://jira.atlassian.com'
    #     with pytest.raises(NoOptionError):
    #         config.get('auth', 'username')
    #         config.get('auth', 'password')
    #     assert not config.get('auth', 'kerberos')
    #     assert config.get('mutt2jira', 'assign')
