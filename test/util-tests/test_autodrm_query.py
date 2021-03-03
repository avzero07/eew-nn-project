'''
Testcases for util.autodrm_query
'''

import sys
import os
import pytest

sys.path.insert(0,os.path.join('..','..'))

from util.autodrm_query import query

def test_query_init():
    query_reference = '''BEGIN
FTP akshay.viswakumar@gmail.com
SUBJECT 2017.eq.event
START_TIME 2017/03/07.15:35:52
DURATION 2100
STA_LIST WSLR,LLLB,HOPB,HOLB,PHC,PACB,EDB,WOSB,NCSB,NTKA,GDR,CBB,OZB,BFSB,PTRF,CLRS,NLLB,GOBB,SYMB,PGC,SNB,VGZ,SHB,WPB
CHAN_LIST *
FORMAT SEED
WAVEFORM
STOP'''
    
    query_obj = query(
           'akshay.viswakumar@gmail.com',
           '2017.eq.event',
           '2017/03/07.15:35:52',
           2100,
           ['WSLR','LLLB','HOPB','HOLB','PHC','PACB','EDB',
               'WOSB','NCSB','NTKA','GDR','CBB','OZB','BFSB',
               'PTRF','CLRS','NLLB','GOBB','SYMB','PGC','SNB',
               'VGZ','SHB','WPB'],
            )
    query_test = query_obj.generate_query()
    assert query_reference.strip() == query_test,"\nReference Query\n{}\nTest Query\n{}".format(query_reference,query_test)
