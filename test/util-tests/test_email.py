'''
Testcases for util.email
'''

import sys
import os
import pytest

sys.path.insert(0,os.path.join('..','..'))

from util.email import email

def test_email():
    email_reference = '''From: Akshay Viswakumar <akviswa7@ece.ubc.ca>
To: autodrm@seismo.nrcan.gc.ca
Cc: akshay.viswakumar@gmail.com
Bcc:
Subject:
Reply-To:

BEGIN
EMAIL akshay.viswakumar@gmail.com
STOP''' 
    email_obj = email('Akshay Viswakumar','akviswa7@ece.ubc.ca',
            'autodrm@seismo.nrcan.gc.ca','',
            "BEGIN\nEMAIL akshay.viswakumar@gmail.com\nSTOP",
            ['akshay.viswakumar@gmail.com'],)
    email_test = email_obj.generate_email()
    assert email_reference.strip() == email_test,"\nReference Email\n{}\n\nTest Email\n{}".format(email_reference,email_test)
