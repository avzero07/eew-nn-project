'''
This module contains functions that are used
to construct formatted emails that are
sent to the CNDC AutoDRM program.
'''

class email:
    def __init__(self,from_name,from_email,to_email,subject,body,
            cc_email=[''],bcc_email=[''],reply_to=['']):
        '''
        Construct the Query Object Using Parameters
        
        Parameters
        ----------
        from_name       :   str
            - Name of sender
        from_email      :   str
            - Email address of sender
        to_email        :   str
            - Email address of receiver
        subject         :   str
            - Subject of Email to be Sent
        body
            - Email body/content
        cc_email        :   list
            - List of Email adresses to be Ccd
            - Empty by default
        bcc_email       :   list
            - List of Email adresses to be Bccd
            - Empty by default
        reply_to        :   list
            - List of Email adresses to directly reply to
            - Empty by default
        '''
        self.from_name = from_name
        self.from_email = from_email
        self.to_email = to_email
        self.subject = subject
        self.body = body
        self.cc_email = cc_email
        self.bcc_email = bcc_email
        self.reply_to = reply_to

    def generate_email_header(self):
        '''
        Constructs and returns the Email header
        '''
        email_header = '\n'.join([
            ' '.join(['From:',self.from_name,''.join(['<',self.from_email,'>'])]),
            ' '.join(['To:',self.to_email]),
            ' '.join(['Cc:',','.join(self.cc_email)]).strip(),
            ' '.join(['Bcc:',','.join(self.bcc_email)]).strip(),
            ' '.join(['Subject:',self.subject]).strip(),
            ' '.join(['Reply-To:',','.join(self.reply_to)]).strip()
            ])
        return email_header

    def generate_email(self):
        '''
        Returns the Email (header+body)
        '''
        header = self.generate_email_header()
        email = '\n\n'.join([header,self.body])
        return email
