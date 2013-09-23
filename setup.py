""" Setup file.

    reddrip - simple reddid image ripper
    Copyright (C) 2013 Nikola Kotur <kotnick+python@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
from setuptools import setup, find_packages

__VERSION__ = "1.2.2"

root_dir = os.path.abspath(os.path.dirname(__file__))
readme_file = os.path.join(root_dir, "README.md")
README = 'Reddrip is Reddit subreddit picture ripper.'
if os.path.exists(readme_file):
    with open(readme_file) as f:
        README = f.read()

setup(name="reddrip",
    version=__VERSION__,
    description="Reddrip is Reddit subreddit picture ripper.",
    long_description=README,
    keywords="reddit crawler",
    author="Nikola Kotur",
    author_email="kotnick+python@gmail.com",
    url="https://github.com/kotnik/reddrip",
    download_url="https://github.com/kotnik/reddrip/archive/v1.1.tar.gz",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=[
        "bin/reddrip",
    ],
    install_requires=[
        "redis",
        "requests",
        "praw",
        "colorama",
        "texttable",
    ],
    platforms="any",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Environment :: Console",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
