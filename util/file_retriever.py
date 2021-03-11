'''
Script to Retrieve and Organize Miniseed Archives
'''

import sys
import os
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

    sta_list = {'WSLR','HOPB','GOBB'}

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

    # TODO: Each Connection in a Separate Thread
    with FTP("ftp.seismo.NRCan.gc.ca") as ftp:
        ftp.login()

        # Start Looping Through List
        day_labels = set()
        for i in range(events.data_frame.shape[0]):
            if (os.getcwd() != dir_root):
                os.chdir(dir_root)
            dt = events.get_date_time(i)
            dt_label = get_day_label(dt)
            if dt_label in day_labels:
                print("Data from {} already present! Skipping".format(dt_label))
                continue

            day_labels.add(dt_label)

            # Check if Year Dir Exists
            year_dir = "{}".format(dt.year)
            if not os.path.isdir(year_dir):
                create_dir(year_dir)
            os.chdir(year_dir)

            # Check if Month Dir Exists
            month_dir = "{:02d}".format(dt.month)
            if not os.path.isdir(month_dir):
                create_dir(month_dir)
            os.chdir(month_dir)

            # Check if Day Dir Exists
            day_dir = "{:02d}".format(dt.day)
            if not os.path.isdir(day_dir):
                create_dir(day_dir)
            os.chdir(day_dir)
            print("Current Local Dir : {}".format(os.getcwd()))

            cd(ftp,"/wfdata/CN/{}/{}/{}/".format(year_dir,month_dir,day_dir))
            remote_file_list = get_dir_list(ftp)

            for f in remote_file_list:
                for sta in sta_list:
                    if sta in f:
                        get_file(ftp,f)

if __name__ == "__main__":
    main()
