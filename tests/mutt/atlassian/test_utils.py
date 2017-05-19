import pytest

from mutt.atlassian.utils import _compact
from mutt.atlassian.utils import get_yes_or_no


class TestUtils:


    def test__compact(self):
        inpt = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua."""
        output = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod
tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua."""
        assert _compact(inpt) == output
        output = """ [...]"""
        assert _compact(inpt, 11) == output
        output = """Lorem [...]"""
        assert _compact(inpt, 12) == output
        output = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod
tempor [...]"""
        assert _compact(inpt, 93) == output


    def test_get_yes_or_no(self, capsys):
        import sys
        print ("hello")
        sys.stderr.write("world\n")
        out, err = capsys.readouterr()
        assert out == "hello\n"
        assert err == "world\n"
        print ("next")
        out, err = capsys.readouterr()
        assert out == "next\n"

        import __builtin__
        __builtin__.raw_input = lambda x: 'y'
        assert get_yes_or_no('')
        __builtin__.raw_input = lambda x: 'n'
        assert not get_yes_or_no('')

        # import pdb; pdb.set_trace()
        # original_raw_input = __builtins__['raw_input']
        # __builtins__['raw_input'] = lambda _: 'yes'
        # print 'y'
        # get_yes_or_no('')
        # assert
        # import pdb; pdb.set_trace()
        # # self.assertEqual(answerReturn(), 'you entered yes')
        # __builtins__['raw_input'] = original_raw_input

        QUESTION = 'Do you know the answer?'
        # assert get_yes_or_no(QUESTION)
        # out, err = capsys.readouterr()
