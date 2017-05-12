# -*- coding: utf-8 -*-
'''

@author: Andreas Schiweck

'''

import argparse
import os
import re
import sys

from jira import JIRA

from mutt.atlassian.application import get_jira
from mutt.atlassian.completer import JIRACompleter
from mutt.atlassian.config import HOME, CONFIG, ISSUEKEY, TERMWIDTH
from mutt.atlassian.config import get_config
from mutt.atlassian.utils import _compact
from mutt.atlassian.utils import get_yes_or_no
from mutt.message import Message

# import logging
# LOG_FILENAME = '/tmp/completer.log'
# logging.basicConfig(
#     filename=LOG_FILENAME,
#     level=logging.DEBUG,
# )


def get_args():
    """
    """
    parser = argparse.ArgumentParser(description='Create/Enhance JIRA issues by emails from mutt.')
    parser.add_argument('--config', help='alternative path to config file (default: %(default)s)',
                        default=CONFIG, metavar='PATH')
    mode = parser.add_argument_group(title='(optional) force a mode')
    group = mode.add_mutually_exclusive_group()
    group.add_argument('-n', '--new', help='create a new issue',
                       action='store_true')
    group.add_argument('-c', '--comment', help='comment an existing issue',
                       action='store_true')
    group.add_argument('-a', '--attachment', help='attach a file to an existing issue',
                       action='store_true')
    group.add_argument('-t', '--transition', help='change the state of an existing issue',
                       action='store_true')
    parser.add_argument('msg', nargs='?', help='message to parse, defaults to <STDIN>',
                        type=argparse.FileType('r'), default=sys.stdin, metavar='MESSAGE')
    return parser.parse_args()


def main():
    """
    """
    args = get_args()
    config = get_config(args.config)
    jira = get_jira(config)
    message = Message().message
    completer = JIRACompleter([])

    # try to clear terminal for interaction
    if config.get('globals', 'clear'):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except:
            pass

    if args.new:
        mode = "[NEW]"
    elif args.comment:
        mode = "[COMMENT]"
    elif args.attachment:
        mode = "[ATTACHMENT]"
    elif args.transition:
        mode = "[TRANSITION]"
    else:
        mode = "[GUESSED]"

    # enhancing an existing issue
    if (re.search(ISSUEKEY, message['subject']) or args.comment or args.attachment or args.transition) \
       and not args.new:

        print "\n%s Enhancing an existing issue..." % mode

        if re.search(ISSUEKEY, message['subject']):
            try:
                issue = jira.issue(re.search(ISSUEKEY, message['subject']).group(1))
            except:
                issue = None
        else:
            issue = None

        # select an issue if forced or search failed
        if not issue:

            def get_issues(search=None):
                # logging.debug('search=%s', search)
                if not search:
                    jql = 'assignee="'+config.get('auth', 'username')+'" AND status != Closed'
                else:
                    s = []
                    words = search.split()
                    for word in words:
                        s.append('summary~"'+word+'*"')
                    jql = ' AND '.join(s)
                issues = {}
                for issue in jira.search_issues(jql):
                    summary = "%s (%s)" % (issue.fields.summary, issue.key)
                    issues[issue.key] = summary.encode('utf-8', errors='ignore')
                return issues
            completer.updater = get_issues

            try:
                print '\nPlease select an issue:'
                issue = raw_input("(issue)> ")
                try:
                    issue = jira.issue(re.search(ISSUEKEY, issue).group(1))
                    # logging.debug('issue=%s', issue)
                except:
                    sys.exit(1)
            except KeyboardInterrupt:
                sys.exit(1)

        transition = None
        if args.transition:
            transitions = {}
            for transition in jira.transitions(issue):
                transitions[transition['id']] = "%s (%s)" % (transition['name'], transition['id'])
            completer.options = transitions

            try:
                print '\nPlease select a transition:'
                transition = raw_input("(transition)> ")
            except KeyboardInterrupt:
                sys.exit(1)
            for key in transitions.keys():
                if transitions[key] == transition:
                    transition = key
                    break

        print '\n{Issue}\n(%s) %s' % (issue.key, _compact(issue.fields.summary, TERMWIDTH - len("(%s) " % issue.key)))

        comment = None
        if message['body'] and not (args.attachment or args.transition):
            print '\n{Comment}\n%s' % _compact(message['body'], TERMWIDTH * 5)
            comment = message['body']
        elif not message['body'] and args.comments:
            print "\nNo body found!"
            sys.exit(1)

        attachments = None
        if len(message['attachments'].keys()) > 0 and not (args.comment or args.transition):
            attachments = '\n'.join([message['attachments'][key]['name'] for key in message['attachments'].keys()])
            print '\n{Attachments}\n%s' % attachments
        elif len(message['attachments'].keys()) == 0 and args.attachment:
            print "\nNo attachment found!"
            sys.exit(1)

        if config.get('mutt2jira', 'assign'):
            print '\n{Assignee}\n%s' % config.get('auth', 'username')

        if get_yes_or_no('Modify the issue?'):

            if transition:
                jira.transition_issue(issue, transition)

            if comment:
                comment = jira.add_comment(issue, comment)

            if attachments:
                for key in message['attachments'].keys():
                    a = message['attachments'][key]
                    data = open(a['tmp'], 'rb')
                    attachment = jira.add_attachment(
                        issue=issue,
                        attachment=data,
                        filename=a['name'])
                    data.close()

            if config.get('mutt2jira', 'assign'):
                jira.assign_issue(issue, config.get('auth', 'username'))

            print "\nEnhanced!"
            sys.exit()
        else:
            print "\nAborted!"
            sys.exit(1)

    # create a new issue
    else:
        print "\n%s Creating a new issue..." % mode

        projects = {}
        for project in jira.projects():
            projects[project.key] = "%s (%s)" % (project.name, project.key)
        completer.options = projects

        try:
            print '\nPlease select a project:'
            project = raw_input("(project)> ")
        except KeyboardInterrupt:
            sys.exit(1)
        for key in projects.keys():
            if projects[key] == project:
                project = jira.project(key)
                break

        itypes = {}
        for itype in project.issueTypes:
            itypes[itype.id] = "%s (%s)" % (itype.name, itype.id)
        completer.options = itypes

        try:
            print '\nPlease select an issue type:'
            itype = raw_input("(issue type)> ")
        except KeyboardInterrupt:
            sys.exit(1)
        for key in itypes.keys():
            if itypes[key] == itype:
                itype = key
                break

        if message['subject']:
            print '\n{Summary}\n%s' % _compact(message['subject'], TERMWIDTH)

        if message['body']:
            print '\n{Description}\n%s' % _compact(message['body'], TERMWIDTH * 5)

        if len(message['attachments'].keys()) > 0:
            attachments = '\n'.join([message['attachments'][key]['name'] for key in message['attachments'].keys()])
            print '\n{Attachments}\n%s' % attachments

        if config.get('mutt2jira', 'assign'):
            print '\n{Assignee}\n%s' % config.get('auth', 'username')

        if get_yes_or_no('Create the issue?'):

            new = {
                'project': {'key': project.key},
                'summary': message['subject'],
                'description': message['body'],
                'issuetype': {'id': itype},
            }

            issue = jira.create_issue(fields=new)

            for key in message['attachments'].keys():
                a = message['attachments'][key]
                data = open(a['tmp'], 'rb')
                attachment = jira.add_attachment(
                    issue=issue,
                    attachment=data,
                    filename=a['name'])
                data.close()

            if config.get('mutt2jira', 'assign'):
                jira.assign_issue(issue, config.get('auth', 'username'))

            print "\nCreated!"
            sys.exit()
        else:
            print "\nAborted!"
            sys.exit(1)
