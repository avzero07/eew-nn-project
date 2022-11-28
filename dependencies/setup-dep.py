'''
Script to Install Dependencies
'''

import os
import sys
import shutil
import tarfile
import subprocess as sp

def install_rdseed():
    # OS Specific Stuff
    '''
    TODO: rdseed was not built to compile
    on windows. Not a priority at this time.
    '''
    print("Platform is {}".format(sys.platform))
    if sys.platform == 'linux' or sys.platform == 'darwin':
        dest_dir = os.path.join('/usr','local','bin')
        rdseed_source_file = "v5.3.1-Mod.tar.gz"
    elif sys.platform == 'win32':
        dest_dir = os.path.join(os.environ['WINDIR'],'system32')
        rdseed_source_file = "v5.3.1-Mod-Win.tar.gz"

    # Change Directory to rdseed/
    cur_dir = os.getcwd()
    os.chdir(os.path.join('rdseed'))
    
    # Extract Tar
    with tarfile.open(rdseed_source_file,"r:gz") as rdseed_tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(rdseed_tar)

    # Change Directory
    os.chdir(os.path.join('rdseed-5.3.1'))

    # Run Make
    op = run_process(['make','clean'])
    print_process_info(op)
    op = run_process(['make'])
    print_process_info(op)

    # Check Output
    op = run_process(['./rdseed','-h'])
    if "d = read data from tape;" in op.stdout.decode():
        print("Make Success; rdseed Seems to be Running!")

    # Move rdseed to directory in PATH
    shutil.move('rdseed',dest_dir)

    # Move Back to Dependencies
    os.chdir(cur_dir)
    op = run_process(['rdseed','-h'])
    if "d = read data from tape;" in op.stdout.decode():
        print("Copy Successful! rdseed accessible from PATH")

def run_process(command_list):
    '''
    Run a Command in Shell and Return Object
    Caller can decide what to do in case of
    error
    '''
    output = sp.run(command_list,stderr=sp.PIPE,stdout=sp.PIPE)
    return output

def print_process_info(op):
    print("Return Code = {}".format(op.returncode))
    print("stdout : \n{}".format(op.stdout.decode()))
    print("stderr : \n{}".format(op.stderr.decode()))

def main():
    install_rdseed()

if __name__ == "__main__":
    main()
