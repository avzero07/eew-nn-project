'''
Code to retrieve files from FTP servers. Uses
ftplib implementation of python3.
'''

import os

def cd(ftp_object,dir="."):
    ftp_object.cwd(dir)

def get_file(ftp_object,filename,target_dir="."):
    with open(os.path.join(target_dir,filename),'wb') as fp:
        ftp_object.retrbinary("RETR {}".format(filename),fp.write)
        print("Downloaded {} to {}".format(filename,target_dir))

def get_dir_list(ftp_object):
    return ftp.nlst()

