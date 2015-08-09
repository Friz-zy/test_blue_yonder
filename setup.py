#!/usr/bin/env python2.7
# coding=utf-8
import sys
import downloader
from subprocess import call
from os.path import join, dirname
from setuptools import setup, find_packages, Command


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = call(['py.test', '--cov', 'downloader', 'tests'])
        raise SystemExit(errno)

def md2rst(path):
    cmd = 'pandoc --from=markdown --to=rst --output={1} {0}'
    rst = path.replace('md', 'rst')
    call(cmd.format(path, rst), shell=True)
    with open(rst) as f:
        rst = f.read()
    return rst

setup(
name='downloader',
version=downloader.__version__,
author = downloader.__author__,
author_email = downloader.__email__,
description = downloader.__description__,
license = downloader.__license__,
keywords = downloader.__keywords__,
url = downloader.__url__,
long_description=md2rst(join(dirname(__file__), 'README.md')),
packages=find_packages(),
cmdclass = {'test': PyTest},
tests_require=['pytest', 'pytest_capturelog', 'pytest-cov'],
install_requires=['gevent', 'argparse', 'PyYAML'],
entry_points={
'console_scripts': [
'downloader = downloader.downloader:main',
]
},
classifiers=[
'Development Status :: 5 - Production/Stable',
'Environment :: Console',
'Intended Audience :: Developers',
'Intended Audience :: System Administrators',
'License :: OSI Approved :: Apache Software License',
'Operating System :: MacOS :: MacOS X',
'Operating System :: Unix',
'Operating System :: POSIX',
'Programming Language :: Python',
'Programming Language :: Python :: 2.7',
'Topic :: System :: Systems Administration',
],
)