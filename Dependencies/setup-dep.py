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
    sp.check_output(['make','clean'],stderr=sp.STDOUT,shell=True)
    sp.check_output(['make'],stderr=sp.STDOUT,shell=True)

    # Check Output
    rdseed_help_op = sp.check_output(['./rdseed','-h'],stderr=sp.STDOUT,shell=True)
    print(rdseed_help_op)

def main():
    install_rdseed()

if __name__ == "__main__":
    main()
