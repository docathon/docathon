#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Docathon community'
SITENAME = 'Docathon'
SITEURL = 'https://bids.github.io/docathon'

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/Docathon'),
          ('GitHub', 'https://github.com/docathon'),)

DEFAULT_PAGINATION = 3

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = "themes/theme"
DISPLAY_HEADER = True
DISPLAY_FOOTER = True
DISPLAY_HOME   = True
DISPLAY_MENU   = True


# provided as examples, they make ‘clean’ urls. used by MENU_INTERNAL_PAGES.
TAGS_URL           = 'tags'
TAGS_SAVE_AS       = 'tags/index.html'
AUTHORS_URL        = 'authors'
AUTHORS_SAVE_AS    = 'authors/index.html'
CATEGORIES_URL     = 'categories'
CATEGORIES_SAVE_AS = 'categories/index.html'
ARCHIVES_URL       = 'archives'
ARCHIVES_SAVE_AS   = 'archives/index.html'


# provided as examples, they make ‘clean’ urls. used by MENU_INTERNAL_PAGES.
TAGS_URL           = 'tags'
TAGS_SAVE_AS       = 'tags/index.html'
AUTHORS_URL        = 'authors'
AUTHORS_SAVE_AS    = 'authors/index.html'
CATEGORIES_URL     = 'categories'
CATEGORIES_SAVE_AS = 'categories/index.html'
ARCHIVES_URL       = 'archives'
ARCHIVES_SAVE_AS   = 'archives/index.html'

# use those if you want pelican standard pages to appear in your menu
MENU_INTERNAL_PAGES = (
#    ('Tags', TAGS_URL, TAGS_SAVE_AS),
#    ('Authors', AUTHORS_URL, AUTHORS_SAVE_AS),
#    ('Categories', CATEGORIES_URL, CATEGORIES_SAVE_AS),
#    ('Archives', ARCHIVES_URL, ARCHIVES_SAVE_AS),
)
# additional menu items
MENUITEMS = (
#    ('GitHub', 'https://github.com/'),
#    ('Linux Kernel', 'https://www.kernel.org/'),
)

STATIC_PATHS = ['images', 'extras/favicon.ico']
HEADER_IMAGE = "logo.svg"

EXTRA_PATH_METADATA = {
    'extras/favicon.ico': {'path': 'favicon.ico'}
}
