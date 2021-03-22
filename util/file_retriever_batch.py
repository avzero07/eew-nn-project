'''
Script to Retrieve and Organize Miniseed Archives
in batches. Designed to be called at the month level.
'''

import sys
import os
import logging
import subprocess as sp
import file_retriever

def main():
    '''
    Arg1        :   Specifies Month Directory to Walk
    '''

    # TODO: Add arg validation
    if len(sys.argv) < 2:
        print("Insufficient Input Arguments!!")
        sys.exit(1)

    # cd into directory
    dir_root = os.getcwd()
    os.chdir(sys.argv[1])
    dir_work = os.getcwd()

    logger_batch = file_retriever.setup_logger("batch_logger","file_retriever_batch.log",
            level=logging.DEBUG)

    logger_batch.debug("Currently in {}".format(dir_work))

    # Init Target List
    day_dir_list = set()

    # List Contents
    dir_contents = os.listdir()

    logger_batch.debug("Walking Through Day Directories")
    # Walk Through Folders and Create Absolute Paths
    for item in dir_contents:
        # Validate Day Directories
        if len(item)!=2:
            continue
        os.chdir(item)
        day_dir_list.add(os.getcwd())
        os.chdir("..")

    # Sort day_dir_list
    day_dir_list = sorted(day_dir_list)

    logger_batch.info("Day Directory List built\n{}".format(day_dir_list))

    # Move Back to dir_root
    os.chdir(dir_root)

    logger_batch.debug("Currently in {}".format(os.getcwd()))

    # Start Walking Through dir_contents
    for day in day_dir_list:
        logger_batch.debug("Executing : file_retriever for {}".format(day))
        # TODO: Consider Using POpen instead
        #file_retriever.main([day])
        op = file_retriever.run_cmd("python3 file_retriever.py"
                " {}".format(day))
        print(op)

if __name__ == "__main__":
    main()
