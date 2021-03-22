'''
Script to Retrieve and Organize Miniseed Archives
'''

import sys
import os
import logging
import datetime
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

import subprocess as sp
import concurrent.futures

def setup_logger(name, log_file, level=logging.INFO):
    '''
    Method to setup custom logger object. Useful when
    needing to simultaneously write to multiple files.
    '''
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

def run_cmd(command_string):
    command_list = command_string.split()
    op = sp.run(command_list,stderr=sp.PIPE,stdout=sp.PIPE)
    return op

def download_file(remote_file_path):
    # TODO: Windows Support
    complete_url = "ftp://ftp.seismo.NRCan.gc.ca{}".format(remote_file_path)
    command_string = "wget {}".format(complete_url)
    op = run_cmd(command_string)
    if not op.returncode:
        rt_string = "Downloaded {}".format(remote_file_path)
    else:
        rt_string = "Failed to Download {}\n{}".format(remote_file_path,op)
    return rt_string

def main(args):
    '''
    Arg1        :   Specifies destination dir root
    '''

    entropy = datetime.datetime.now().microsecond

    # TODO: Add arg validation
    if len(args) < 1:
        print("Insufficient Input Arguments!!")
        sys.exit(1)

    # cd into directory
    os.chdir(args[0])
    dir_root = os.getcwd()

    logger = setup_logger("day_level_logger_{}".format(entropy),"file_retriever.log"
            ,level=logging.DEBUG)

    logger.debug("Currently in {}".format(dir_root))

    # Read the dl_manifest into a List
    # TODO: check if dl_manifest exists locally
    logger.debug("Looking at the Manifest File : {}".format("dl_path.txt"))
    with open('dl_path.txt','r') as dlf:
        dl_manifest = dlf.readlines()

    logger.debug("Manifest File has been read!")

    logger.debug("Commencing File Download")
    # Concurrent Execution
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for rt_string in executor.map(download_file,dl_manifest):
            logger.info(rt_string)

    logger.debug("Downloads Complete!")

if __name__ == "__main__":
    main(sys.argv[1:])
