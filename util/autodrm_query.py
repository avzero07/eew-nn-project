'''
This module contains functions that are used
to construct queries for the CNDC AutoDRM
program.
'''

class query:
    def __init__(self,querier_email,subject,start_time,duration,sta_list,chan_list=['*'],
            return_format='SEED',return_medium='FTP'):
        '''
        Construct the Query Object Using Parameters
        
        Parameters
        ----------
        querier_email   :   str
            - Email address of querier
            - AutoDRM sends response to this address
        subject         :   str
            - Email Subject to Be Used for with the Query
        start_time      :   str
            - Timestamp for earliest piece of data, 'yyyy/mm/dd.hh:mm:ss'
        duration        :   int
            - Duration in seconds
        sta_list        :   list
            - List of strings. Each item is a station identifier (eg: HOPB)
        chan_list       :   list
            - List of strings. Each item is a channel identifier (eg: HOPB)
        return_format   :   str
            - Format of Archive Returned by AutoDRM.
            - Default is 'SEED'
        return_medium   :   str
            - Specifies how the medium of return {EMAIL | FTP}
            - Default is 'FTP'
        '''
        self.return_medium = return_medium
        self.subject = subject
        self.start_time = start_time
        self.duration = duration
        self.sta_list = sta_list
        self.chan_list = chan_list
        self.querier_email = querier_email
        self.return_format = return_format

    def generate_query(self):
        '''
        Construct a Query Based on Object Parameters
        '''
        query = '\n'.join([
            'BEGIN',
            ' '.join([self.return_medium,self.querier_email]),
            ' '.join(['SUBJECT',self.subject]),
            ' '.join(['START_TIME',self.start_time]),
            ' '.join(['DURATION',str(self.duration)]),
            ' '.join(['STA_LIST',','.join(self.sta_list)]), 
            ' '.join(['CHAN_LIST',','.join(self.chan_list)]),
            ' '.join(['FORMAT',self.return_format]),
            'WAVEFORM',
            'STOP'
            ])
        return query
