#!/usr/bin/env python2.7
# coding=utf-8
"""This is part of [test_blue_yonder](https://github.com/Friz-zy/test_blue_yonder)

License: Apache 2.0
Copyright (c) 2015 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

"""


import os
import sys
import urllib
import logging

import gevent
from gevent import monkey, pool
monkey.patch_all()


logging.basicConfig(
    format=u'%(asctime)s  downloader\t%(levelname)-8s\t%(message)s',
    datefmt='%d %b %Y %H:%M:%S',
    stream=sys.stdout, # will be replacing by filename
    #filename= 'downloader.log',
    #filemode='a',
    level=logging.INFO,
)


def cli(arguments=sys.argv):
    pass

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
    name = os.path.join(output_dir, link.split('/')[-1])
    logging.debug('Start downloading: %s as %s', link, name)
    try:
        urllib.urlretrieve(url=link, filename=name)
        logging.info('Finishing downloading: %s as %s', link, name)
        return 0
    except Exception as e:
        logging.error('Can not download %s: %s', link, e)
        return link

def async_map(function, arguments, pool_size=None):
    """Wrapper over gevent.pool.Pool

    Args:
      function (object): function for execution
      arguments (iterable): list of argiments for function
      pool_size (int): max pool size,
        default is None - unlimited

    Return:
      list of resulsts

    """
    pl = pool.Pool(pool_size)
    return pl.map(function, arguments)

def main(arguments=sys.argv):
    pass


if '__name__' == '__main__':
    main()