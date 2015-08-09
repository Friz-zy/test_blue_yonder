#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Requirements specification for the downloader

This is part of [test_blue_yonder](https://github.com/Friz-zy/test_blue_yonder)

License: Apache 2.0
Copyright (c) 2015 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

"""


import os
import pytest
import hashlib
import logging
import downloader


def test_dowload_files_from_internet(tmpdir, caplog, file, links):
    """Test for downloader.main

    Assertions:
      all links exists in log
      files stored or exception exists in log

    """
    output_dir = str(tmpdir.mkdir('download'))
    arguments = ['downloader', str(file), output_dir]
    downloader.main(arguments)

    caplog.setLevel(logging.INFO)
    out = caplog.records()
    info = '\n'.join([o.message for o in out if o.levelname == 'INFO'])
    errors = [o.message for o in out if o.levelname == 'ERROR']
    error = '\n'.join(errors)

    listdir = os.listdir(output_dir)

    # all links exists in log
    assert all(link in info for link in links) or \
        all(link in error for link in links)

    for link in links:
        name = link.split('/')[-1]
        # files stored or exception exists in log
        assert name in listdir or link in error

def test_parse_file(tmpdir, caplog, file, links):
    """Test for downloader.cli

    Assertions:
      all links exists in tuple

    """
    output_dir = str(tmpdir.mkdir('download'))
    arguments = ['downloader', str(file), output_dir]
    args = downloader.cli(arguments)
    print args.links
    assert args.links == [l for l in links]

def test_download_one_file_to_the_right_place(tmpdir, caplog, links):
    """Test for downloader.get_file

    Assertions:
      file stored to the right place or exception exists in log
      file stored with right md5 sum

    """
    link = links[0]
    output_dir = str(tmpdir.mkdir('download'))
    downloader.get_file(link, output_dir)
    caplog.setLevel(logging.ERROR)
    out = caplog.records()[0]
    listdir = os.listdir(output_dir)
    assert len(listdir) == 1 or link in out.message
    if listdir:
        name = listdir[0]
        assert name == link.split('/')[-1]

def test_async_map_run_all_functions():
    """Test for downloader.async_map

    Assertions:
      async_map run all functions

    """
    function = lambda x, y: (x, y)
    arguments = [(x, x) for x in xrange(0, 9)]
    pool_size = None
    resulsts = downloader.async_map(
        function, arguments, pool_size
        )
    assert sorted(resulsts) == zip(range(0, 9), range(0,9))