'''
Script to Retrieve and Organize Miniseed Archives
'''

import sys
import os
import logging
import subprocess as sp
import concurrent.futures

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
        rt_string = "Failed to Download {}".format(remote_file_path)
    return rt_string

def main(args):
    '''
    Arg1        :   Specifies destination dir root
    '''

    # TODO: Add arg validation
    if len(args) < 1:
        print("Insufficient Input Arguments!!")
        sys.exit(1)

    # cd into directory
    os.chdir(args[0])
    dir_root = os.getcwd()

    logging.basicConfig(filename="file_retriever.log",filemode="w+",
            level=logging.DEBUG)

    logging.debug("Currently in {}".format(dir_root))

    # Read the dl_manifest into a List
    # TODO: check if dl_manifest exists locally
    logging.debug("Looking at the Manifest File : {}".format("dl_path.txt"))
    with open('dl_path.txt','r') as dlf:
        dl_manifest = dlf.readlines()

    logging.debug("Manifest File has been read!")

    logging.debug("Commencing File Download")
    # Concurrent Execution
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for rt_string in executor.map(download_file,dl_manifest):
            logging.info(rt_string)

    logging.debug("Downloads Complete!")

if __name__ == "__main__":
    main(sys.argv[1:])
