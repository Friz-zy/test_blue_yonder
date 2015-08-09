#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Requirements specification for the downloader"""

__author__ = 'Filipp Frizzy'
__credits__ = ["Filipp Frizzy"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "Filipp Frizzy"
__email__ = "filipp.s.frizzy@gmail.com"
__status__ = "Development"


import pytest


@pytest.fixture(scope="session")
def links():
    links = [
        ('https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Clematis_macro_1.JPG/120px-Clematis_macro_1.JPG',
        'e47b760fde49158647d4ea4a68fbc7d8'),
        ('https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Coffea_canephora_berries.JPG/120px-Coffea_canephora_berries.JPG',
        'b7b505794e32cefa5cec399ca4f211a7'),
        ('https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Elaeagnus_umbellata_berries.JPG/120px-Elaeagnus_umbellata_berries.JPG',
        '6ae999fa8aa41c01c2a5efa21c87b116'),
        ]
    return links

@pytest.fixture()
def file(tmpdir, links):
    p = tmpdir.join("links.txt")
    p.write(['%s\n' % l[0] for l in links])
    return str(p)