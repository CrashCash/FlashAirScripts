# put files on Toshiba FlashAir SD card via wi-fi
# see https://www.flashair-developers.com/en/documents/api/

import os
import sys
import argparse
import requests
import configparser

class card:
    def __init__(self):
        self.config_file=os.path.expanduser('~/.flashair')
        self.config=configparser.ConfigParser()
        self.config.read(self.config_file)
        self.def_address=self.config['DEFAULT'].get('address', None)
        self.def_directory=self.config['DEFAULT'].get('directory', '/')
        self.def_sort=self.config['DEFAULT'].get('sort', 'a')

        self.parser=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.parser.add_argument('-a', '--address', help='card network address', default=self.def_address)

    def setup(self):
        self.args=self.parser.parse_args()
        self.address=self.args.address
        if 'directory' not in self.args.__dict__:
            self.args.directory=self.def_directory
        self.dir=self.args.directory
        if 'sort' not in self.args.__dict__:
            self.args.sort=self.def_sort
        self.sort=self.args.sort

        if self.address == None:
            print('you must supply a network address for the card')
            exit(1)

        # if values have changed, write them back as defaults
        if self.address != self.def_address or self.dir != self.def_directory or self.args.sort != self.def_sort:
            self.config['DEFAULT']['address']=self.address
            self.config['DEFAULT']['directory']=self.dir
            self.config['DEFAULT']['sort']=self.args.sort
            with open(self.config_file, 'w') as f:
                self.config.write(f)

        # no trailing slash in directory
        if self.dir and self.dir[-1] == '/':
            self.dir=self.dir[:-1]

        # must have leading slash in directory
        if not self.dir or self.dir[0] != '/':
            self.dir='/'+self.dir

    def get_files(self):
        self.files=[]
        r=requests.get('http://'+self.address+'/command.cgi?op=100&DIR='+self.dir)
        if not r:
            if r.status_code == 404:
                print('no such directory:', self.dir)
            else:
                print('error', r.status_code)
            sys.exit(1)

        i=len(self.dir)
        if i > 1:
            i+=1
        for line in r.text.splitlines()[1:]:
            # this code has to handle commas in file name and directory name. in data that's comma-delimited
            first, size, attrib, date, time=line.rsplit(',', 4)
            file=first[i:]
            self.files.append((file, int(size), int(attrib)))
