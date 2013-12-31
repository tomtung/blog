#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

RELATIVE_URLS = False

FEED_RSS = 'feed/index.html'
FEED_ATOM = 'feed/atom.xml'
FEED_ALL_ATOM = 'feed/all.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "tomtung"
GOOGLE_ANALYTICS = "UA-12852556-1"
