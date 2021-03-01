'''
Script to Install Dependencies
'''

import os
import tarfile
import subprocess as sp

def install_rdseed():
    # Change Directory to rdseed/
    cur_dir = os.getcwd()
    os.chdir(os.path.join('rdseed'))
    
    # Extract Tar
    with tarfile.open("v5.3.1-Mod.tar.gz","r:gz") as rdseed_tar:
        rdseed_tar.extractall()

    # Change Directory
    os.chdir(os.path.join('rdseed-5.3.1'))

    # Run Make
    op = run_process(['make','clean'])
    op = run_process(['make'])

    # Check Output
    op = (['./rdseed','-h'])
    print(op.stdout.decode())

def run_process(command_list):
    '''
    Run a Command in Shell and Return Object
    Caller can decide what to do in case of
    error
    '''
    output = sp.run(command_list,stderr=sp.PIPE,stdout=sp.PIPE)
    return output

def main():
    install_rdseed()

if __name__ == "__main__":
    main()
