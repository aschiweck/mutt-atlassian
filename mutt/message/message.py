# -*- coding: utf-8 -*-
'''

@author: Andreas Schiweck

'''

import email
import sys
import html2text
import tempfile

from email.header import decode_header


class Message(object):
    """
    """

    def __init__(self):
        """
        """
        msg = sys.stdin.read()
        sys.stdin = open('/dev/tty')
        self.raw = email.message_from_string(msg)
        self.message = self.parse(self.raw)


    def parse(self, msg):
        """
        """
        message = {
            'subject': '',
            'body': '',
            'attachments': {},
        }

        # body/ attachments
        if msg.is_multipart():
            counter = 0
            for part in msg.walk():
                c_type = part.get_content_type()
                c_disp = part.get('Content-Disposition')
                charset = part.get_content_charset() if part.get_content_charset() else 'ascii'

                # multipart/* are just containers
                if part.get_content_maintype() == 'multipart':
                    continue

                # prefer existing text/plain as message body
                if c_type == 'text/plain' and c_disp != 'attachment':
                    message['body'] = unicode(part.get_payload(decode=True), charset, errors='ignore')
                    continue

                # extract text form text/html if needed
                if c_type == 'text/html' and not message.get('body', None) and c_disp != 'attachment':
                    message['body'] = html2text.html2text(
                        unicode(part.get_payload(decode=True), charset, errors='ignore'))
                    continue

                # extract and identify file attachments
                filename = ''
                for line in decode_header(part.get_filename()):
                    encoding = line[1] if line[1] else 'ascii'
                    filename += unicode(line[0], encoding, errors='ignore')
                if not filename:
                    ext = mimetypes.guess_extension(c_type)
                    if not ext:
                        # Use a generic bag-of-bits extension
                        ext = '.bin'
                    filename = 'attachment-%03d%s' % (counter, ext)
                try:
                    data = tempfile.NamedTemporaryFile()
                    data.write(part.get_payload(decode=True))
                except:
                    data.close()
                    sys.exit(1)
                data.seek(0)
                message['attachments'][counter] = {'name': filename, 'file': data, 'tmp': data.name}
                counter += 1

        else:
            charset = msg.get_content_charset() if msg.get_content_charset() else 'ascii'
            message['body'] = unicode(msg.get_payload(decode=True), charset, errors='ignore')

        # subject
        subject = ''
        for line in decode_header(msg["Subject"]):
            encoding = line[1] if line[1] else 'ascii'
            subject += unicode(line[0], encoding, errors='ignore')
        message['subject'] = subject if subject else 'No subject found!'

        return message
