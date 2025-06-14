#!/usr/bin/env python
# -*- coding: utf-8 -*- #
# Simple Build Configuration for Testing

AUTHOR = 'AI Blog System'
SITENAME = 'AI Generated Blog'
SITEURL = 'https://vons.netlify.app'
SITE_DESCRIPTION = 'Fresh insights, generated daily through AI'

PATH = 'content'
TIMEZONE = 'UTC'
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (
    ('GitHub', 'https://github.com'),
    ('RSS', '/feeds/all.atom.xml'),
)

DEFAULT_PAGINATION = 10

# Theme
THEME = 'themes/aiblog'

# Static paths
STATIC_PATHS = ['images', 'extra']

# Output path
OUTPUT_PATH = 'output/'

# Clean output directory
DELETE_OUTPUT_DIRECTORY = True

# Disable plugins for simple build
PLUGINS = []

# Basic settings
RELATIVE_URLS = False
CACHE_CONTENT = False
LOAD_CONTENT_CACHE = False

# Article settings
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'

# Page settings  
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# Archive settings
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

# Disable unnecessary features for testing
CATEGORY_SAVE_AS = ''
TAG_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
ARCHIVES_SAVE_AS = 'archives/index.html'

# Custom variables for the theme
CUSTOM_VARS = {
    'site_description': 'Fresh insights, generated daily through AI',
    'meta_keywords': 'AI, artificial intelligence, technology, productivity, automation, blog',
    'twitter_username': 'aiblog',
    'environment': 'test',
}

# AI Blog Configuration
AI_BLOG_CONFIG = {
    'show_reading_time': True,
    'show_categories': True,
    'show_tags': True,
    'show_social_share': True,
    'max_related_posts': 3,
    'google_analytics': None,  # Disable for testing
} 