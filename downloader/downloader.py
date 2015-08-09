#!/usr/bin/env python2.7
# coding=utf-8
"""This is part of [test_blue_yonder](https://github.com/Friz-zy/test_blue_yonder)

License: Apache 2.0
Copyright (c) 2015 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

"""


from gevent import monkey, pool
monkey.patch_all()

import os
import sys
import shutil       
import logging
import requests
import argparse


logging.basicConfig(
    format=u'%(asctime)s  downloader\t%(levelname)-8s\t%(message)s',
    datefmt='%d %b %Y %H:%M:%S',
    stream=sys.stdout, # will be replacing by filename
    #filename= 'downloader.log',
    #filemode='a',
    level=logging.INFO,
)


def cli(arguments=sys.argv):
    """Cli with argparse

    Args:
      arguments (tuple): arguments for cli,
        default is sys.argv

    Return:
      argparse namespace object like args

    """
    def loader(string):
        if os.path.exists(string):
            with open(string) as s:
                return s.read().splitlines()
        return string.split(',')

    if arguments != sys.argv:
        sys.argv = arguments

    parser = argparse.ArgumentParser(
        description='Download files from the internet.'
        )
    parser.add_argument('links', type=loader,
                    help='Path to file with links '
                    'or links separated by commas'
                    )
    parser.add_argument('destination', type=str,
                    default=os.getcwd(), nargs='?',
                    help='Save path, default is current dir'
                    )

    return parser.parse_args()

def get_file(link, output_dir=os.getcwd()):
    """Download file from internet

    Args:
      link (str): web url
      output_dir (str): directory for downloading,
        current dir is default

    Return:
      0 if success
      link if fail

    """
    print link
    name = os.path.join(output_dir, link.split('/')[-1])
    logging.debug('Start downloading: %s as %s', link, name)
    try:
        # use request instead of urllib because of bug
        # https://github.com/Code4SA/address2ward/issues/14
        r = requests.get(link, stream=True)
        if r.status_code == 200:
            with open(name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            logging.info('Finishing downloading: %s as %s',
                         link, name
                         )
            return 0
        else:
            logging.error('Can not download %s: status %s', 
                          link, r.status_code
                          )
    except Exception as e:
        logging.error('Can not download %s: %s', link, e)
        return link

def async_map(function, arguments, pool_size=None):
    """Wrapper over gevent.pool.Pool

    Allow use functions with multiple arguments.

    Args:
      function (object): function for execution
      arguments (iterable): list of argiments for function
      pool_size (int): max pool size,
        default is None - unlimited

    Return:
      list of resulsts

    """
    pl = pool.Pool(pool_size)
    return pl.map(lambda args: function(*args), arguments)

def main(arguments=sys.argv):
    """Downloader

    Args:
      arguments (tuple): arguments for cli,
        default is sys.argv

    Return:
      0 if all links succesfully downloaded
      1 otherwise

    """
    args = cli(arguments)
    args = [(link, args.destination) for link in args.links]
    if any(async_map(get_file, args)):
        return 1
    return 0


if '__name__' == '__main__':
    main()