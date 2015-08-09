#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Requirements specification for the downloader

This is part of [test_blue_yonder](https://github.com/Friz-zy/test_blue_yonder)

License: Apache 2.0
Copyright (c) 2015 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

"""


import pytest


@pytest.fixture(scope="session")
def links():
    links = [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Clematis_macro_1.JPG/120px-Clematis_macro_1.JPG',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Coffea_canephora_berries.JPG/120px-Coffea_canephora_berries.JPG',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Elaeagnus_umbellata_berries.JPG/120px-Elaeagnus_umbellata_berries.JPG',
        ]
    return links

@pytest.fixture()
def file(tmpdir, links):
    p = tmpdir.join("links.txt")
    p.write('\n'.join([l for l in links]))
    return str(p)