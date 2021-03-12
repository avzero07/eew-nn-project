'''
Script to Retrieve and Organize Miniseed Archives
'''

import sys
import os
import logging
from ftplib import FTP
from event_parser import eq_events
from ftp import cd, get_file, get_dir_list

def create_dir(name,path='.'):
    dest_dir = os.path.join(path,name) # TODO: OS agnostic?
    os.mkdir(dest_dir)

def get_day_label(dt_object):
    return "{}-{}-{}".format(dt_object.year,dt_object.month,dt_object.day)

def main():
    '''
    Arg1        :   Specifies the Event CSV File
    Arg2        :   Specifies name of destination dir root
    '''

    sta_list =  {
            'WSLR','LLLB','HOPB','HOLB','PHC','PACB','EDB','WOSB','NCSB'
            ,'NTKA','GDR','CBB','OZB','BFSB','PTRF','CLRS','NLLB','GOBB'
            ,'SYMB','PGC','SNB','VGZ','SHB','WPB'
                }

    # TODO: Add arg validation
    if len(sys.argv) < 3:
        print("Insufficient Input Arguments!!")
        sys.exit(1)

    # Load Events and Init Dataframe
    event_file = sys.argv[1]
    events = eq_events(event_file)

    # Create Root Directory and cd into it
    if not os.path.isdir(sys.argv[2]):
        create_dir(sys.argv[2])
    os.chdir(sys.argv[2])
    dir_root = os.getcwd()

    # Init Logging
    logging.basicConfig(filename="file_retriever_prep.log",filemode="w+",
            level=logging.DEBUG)

    logging.debug("Currently in {}".format(dir_root))

    # Start Looping Through List
    logging.debug("Looping Through List of Events")
    day_labels = set()
    for i in range(events.data_frame.shape[0]):
        if (os.getcwd() != dir_root):
            os.chdir(dir_root)
        dt = events.get_date_time(i)
        dt_label = get_day_label(dt)
        if dt_label in day_labels:
            logging.debug("Data from {} already present! Skipping".format(dt_label))
            continue

        day_labels.add(dt_label)

        # Check if Year Dir Exists
        year_dir = "{}".format(dt.year)
        if not os.path.isdir(year_dir):
            logging.info("Creating Directory {} in {}".format(year_dir,os.getcwd()))
            create_dir(year_dir)
        os.chdir(year_dir)

        # Check if Month Dir Exists
        month_dir = "{:02d}".format(dt.month)
        if not os.path.isdir(month_dir):
            logging.info("Creating Directory {} in {}".format(month_dir,os.getcwd()))
            create_dir(month_dir)
        os.chdir(month_dir)

        # Check if Day Dir Exists
        day_dir = "{:02d}".format(dt.day)
        if not os.path.isdir(day_dir):
            logging.info("Creating Directory {} in {}".format(day_dir,os.getcwd()))
            create_dir(day_dir)
        os.chdir(day_dir)
        logging.debug("Current Local Dir : {}".format(os.getcwd()))

        with FTP("ftp.seismo.NRCan.gc.ca") as ftp:
            ftp.login()
            cd(ftp,"/wfdata/CN/{}/{}/{}/".format(year_dir,month_dir,day_dir))
            remote_file_list = sorted(get_dir_list(ftp))
            remote_dir = ftp.pwd()

        logging.debug("Creating Manifest File : {} in {}".format("dl_path.txt",
                                os.getcwd()))
        with open('dl_path.txt','w+') as op_file:
            for f in remote_file_list:
                for sta in sta_list:
                    if sta in f:
                        op_file.write("{}/{}\n".format(remote_dir,f))
        logging.debug("Prepped Manifest File : {} in {}".format("dl_path.txt",
                                os.getcwd()))

if __name__ == "__main__":
    main()
