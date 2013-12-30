#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'逆铭 (tomtung)'
SITENAME = u'~/blog'
SITEURL = 'http://blog.tomtung.com'

TIMEZONE = 'Asia/Shanghai'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True


# Custimizations

PATH = 'content'

ARTICLE_DIR = 'posts'

DOCUTILS_SETTINGS = {'math_output':'MathJax'}

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'

TYPOGRIFY = True

DIRECT_TEMPLATES = ('index', 'archives', 'tags')
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'

ARCHIVES_URL = '/archive'
ARCHIVES_SAVE_AS = 'archive/index.html'

TAGS_URL = '/tags'
TAGS_SAVE_AS = 'tags/index.html'

DISPLAY_CATEGORIES_ON_MENU = False
USE_FOLDER_AS_CATEGORY = False

LOCALE = (
	'chn', 'usa',  					# On Windows
    'zh_CN.UTF-8', 'en_US.UTF-8'    # On Unix/Linux
)

DATE_FORMATS = {
    'en': '%Y-%m-%d',
    'zh': '%Y-%m-%d',
}

STATIC_PATHS = ['images', 'extra/favicon.png']
EXTRA_PATH_METADATA = {'extra/favicon.png': {'path': 'favicon.png'}}

THEME = './theme/pelican-minga'

# Theme-specific

ENABLE_MATHJAX = True
GITHUB_URL = 'https://github.com/tomtung'
TWITTER_URL = 'https://twitter.com/tomtung'
DOUBAN_URL = 'http://www.douban.com/people/tomtung'
WEIBO_URL = 'http://www.weibo.com/1245986775'
