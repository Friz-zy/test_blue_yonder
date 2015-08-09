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
import downloader


def test_dowload_files_from_internet(tmpdir, capsys, file, links):
    """Test for downloader.main

    Assertions:
      all links exists in log
      files stored or exception exists in log
      files stored with right md5 sum

    """
    output_dir = str(tmpdir.mkdir('download'))
    arguments = ['downloader', str(file), output_dir]
    downloader.main(arguments)
    out, err = capsys.readouterr()
    listdir = os.listdir(output_dir)
    assert all(link[0] in out for link in links)
    assert len(listdir) == len(links) or 'ERROR' in out
    for link in links:
        name = link[0].split('/')[-1]
        assert name in listdir or (link[0] in out and 'ERROR' in out)
        if name not in listdir:
            continue
        with open(os.path.join(output_dir, name), 'rb') as f:
            digest = hashlib.md5(f.read()).digest()
        assert digest == link[1]

def test_parse_file(tmpdir, capsys, file, links):
    """Test for downloader.cli

    Assertions:
      all links exists in tuple

    """
    output_dir = str(tmpdir.mkdir('download'))
    arguments = ['downloader', str(file), output_dir]
    args = downloader.cli(arguments)
    assert args.links == [l[0] for l in links]

def test_download_one_file_to_the_right_place(tmpdir, capsys, links):
    """Test for downloader.get_file

    Assertions:
      file stored to the right place or exception exists in log
      file stored with right md5 sum

    """
    link = links[0][0]
    mdsum = links[0][1]
    output_dir = str(tmpdir.mkdir('download'))
    downloader.get_file(link, output_dir)
    out, err = capsys.readouterr()
    listdir = os.listdir(output_dir)
    assert len(listdir) == 1 or (link in out and 'ERROR' in out)
    name = listdir[0]
    assert name == link.split('/')[-1] or (link in out and 'ERROR' in out)
    with open(os.path.join(output_dir, name), 'rb') as f:
        digest = hashlib.md5(f.read()).digest()
    assert digest == mdsum

def test_async_map_run_all_functions():
    """Test for downloader.async_map

    Assertions:
      async_map run all functions

    """
    function = lambda x: x
    arguments = xrange(0, 9)
    pool_size = 2
    resulsts = downloader.async_map(
        function, arguments, pool_size
        )
    assert sorted(resulsts) == xrange(0, 9)