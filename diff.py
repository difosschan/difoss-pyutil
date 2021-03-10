#!env python3
# -*- coding:utf-8 -*-
# author: difosschan
#
__all__ = ('dir_diff',)

from util import *

from os.path import join as path_join
import os
import click
from typing import *
import time
import tarfile

CWD=os.getcwd()
EXCLUDE_DIRS=['.git', '.idea', '__pycache__', 'build', 'eggs', '.eggs', 'wheels', 'vendor', 'phpmyadmin']
EXCLUDE_FILES: List[str]=[]
EXCLUDE_EXTENSIONS: List[str]=[]
INCLUDE_EXTENSIONS: List[str]=['.php']

def G(key: str, default=None) -> Any:
    '''
    get globals by <key>
    :param key: key of globals, usually in uppercase
    '''
    return globals().get(key, default)


def dir_diff(old_dir: str, new_dir: str):

    diff_rel_files = []

    _, old_files = walk(old_dir, exclude_dirs=G('EXCLUDE_DIRS'),
                        exclude_files=G('EXCLUDE_FILES'), include_extensions=G('INCLUDE_EXTENSIONS'))
    _, new_files = walk(new_dir, exclude_dirs=G('EXCLUDE_DIRS'),
                        exclude_files=G('EXCLUDE_FILES'), include_extensions=G('INCLUDE_EXTENSIONS'))

    old_rel_files = [a[a.find('/')+1:] for a in old_files]
    new_rel_files = [a[a.find('/')+1:] for a in new_files]

    addeds = list(set(new_rel_files).difference(set(old_rel_files)))
    deleteds = list(set(old_rel_files).difference(set(new_rel_files)))

    for x in new_rel_files:
        if is_different(x, old_dir, new_dir):
            diff_rel_files.append(x)
            P("Detect difference", file=x, _level='info')

    return diff_rel_files


def is_different(f, d1, d2) -> bool:
    f1 = path_join(d1, f)
    f2 = path_join(d2, f)
    st1 = dump(f1)
    st2 = dump(f2)
    if st1.get('size', 0) != st2.get('size', 0):
        return True

    with open(f1, 'r') as file1:
        with open(f2, 'r') as file2:
            diff = set(file1).difference(file2)
    return True if diff else False

def dump(f: str) -> Dict:
    mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime = os.stat(f)
    return dict(mode=mode, ino=ino, dev=dev, nlink=nlink, uid=uid, gid=gid, size=size,
                atime=atime, mtime=mtime, ctime=ctime)

# --------------------------------------------------------------------------------
def set_global(ctx, param, value):
    name=param.human_readable_name
    globalVarName = str(name).upper()
    globals()[globalVarName]=value
    return value

def set_debug(ctx, param, value):
    set_printable(value)
    set_global(ctx, param, value)
    return value

@click.command()
@click.option('-d', '--debug', help='print debug info', is_flag=True, callback=set_debug)
@click.argument('old_dir')
@click.argument('new_dir')
def cmd_diff(debug: bool,
             old_dir: str,
             new_dir: str):
    diff_rel_files = dir_diff(old_dir, new_dir)
    P(f'Compared with the old directory <{old_dir}>,'
      f' the new directory <{new_dir}> changes files as follows.',
      files=diff_rel_files,
      _must=True, _level='info')


@click.command()
@click.option('-d', '--debug', help='print debug info', is_flag=True, callback=set_debug)
@click.argument('old_dir')
@click.argument('new_dir')
def cmd_tar(debug: bool,
            old_dir: str,
            new_dir: str):
    files = dir_diff(old_dir, new_dir)
    # Create filename according to timestamp
    time_in_file = time.strftime('%Y-%m-%d-%H%M%S', time.gmtime())
    archive_fn = f'{new_dir}-{time_in_file}-byRuiRong.tar.gz'
    tar = tarfile.open(archive_fn, 'w:gz')
    # Add files into archive
    for x in files:
        tar.add(path_join(new_dir, x), arcname=x)
    tar.close()
    P('archive file done.', filename=archive_fn, _level='info', _must=True)


@click.group()
def main():
    pass

main.add_command(cmd_diff, name='diff')
main.add_command(cmd_tar, name='tar')

if __name__ == '__main__':
    main()