'''
Script to Install Dependencies
'''

import os
import tarfile

def install_rdseed():
    # Change Directory to rdseed/
    cur_dir = os.getcwd()
    os.chdir(os.path.join('rdseed'))
    
    # Extract Tar
    with tarfile.open("v5.3.1-Mod.tar.gz","r:gz") as rdseed_tar:
        rdseed_tar.extractall()

def main():
    install_rdseed()

if __name__ == "__main__":
    main()
