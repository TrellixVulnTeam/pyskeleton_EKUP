#!/usr/bin/env python
# -*-coding:utf-8-*-

import sys
import argparse
import os
import os.path
import tarfile
import shutil
from pyskeleton import __version__
from pkg_resources import resource_filename


class Parser(argparse.ArgumentParser):
    def __init__(self, **kwargs):
        super(Parser, self).__init__(**kwargs)


DESCRIPTION = """
will create a python module skeleton
"""


def main():
    parser = Parser(description=DESCRIPTION)
    parser.add_argument('name', help='the target proejct name')
    parser.add_argument('-v', '--version',
                        action='version', version=__version__)
    args = parser.parse_args()
    project_name = args.name

    try:
        os.mkdir(project_name)
        os.chdir(project_name)
    except FileExistsError as e:
        print('file exists error')
        sys.exit(1)

    # tar unzip
    with tarfile.open(
            resource_filename("pyskeleton", "pyskeleton.tar.gz")) as tar:
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
            
        
        safe_extract(tar)

    # make dir
    os.makedirs(f'{project_name}')

    pyfile = resource_filename("pyskeleton", "__init__.py")

    shutil.copy(pyfile, f'{project_name}')

    print('great, create {0} succeed'.format(project_name))
