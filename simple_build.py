#!/usr/bin/env python
# -*- coding: utf-8 -*- #
# Simple Build Configuration for Testing

import re

AUTHOR = 'AI Blog System'
SITENAME = 'AI Generated Blog'
SITEURL = ''
SITE_DESCRIPTION = 'Fresh insights, generated daily through AI'

PATH = 'content'
TIMEZONE = 'UTC'
DEFAULT_LANG = 'en'

# Custom Jinja2 Functions
def calculate_reading_time(content):
    """Calculate reading time for content (fallback function)"""
    if not content:
        return 1
    
    # Remove HTML tags and get plain text
    clean_text = re.sub(r'<[^>]+>', '', str(content))
    word_count = len(clean_text.split())
    
    # Average reading speed is 200 words per minute
    reading_time = max(1, round(word_count / 200))
    return reading_time

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

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

# Output path
OUTPUT_PATH = 'output/'

# Clean output directory
DELETE_OUTPUT_DIRECTORY = True

# Disable plugins for simple build
PLUGINS = []

# Basic settings
RELATIVE_URLS = True
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

# Page generation
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
AUTHOR_SAVE_AS = ''
ARCHIVES_SAVE_AS = 'archives/index.html'

# Direct templates
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'archives']

# Custom variables for the theme
CUSTOM_VARS = {
    'site_description': 'Fresh insights, generated daily through AI',
    'meta_keywords': 'AI, artificial intelligence, technology, productivity, automation, blog',
    'twitter_username': 'aiblog',
    'environment': 'test',
}

# Jinja2 Environment Settings
JINJA_ENVIRONMENT = {
    'trim_blocks': True,
    'lstrip_blocks': True,
}

# Add custom filters
JINJA_FILTERS = {
    'calculate_reading_time': calculate_reading_time,
}

# Navigation
MENUITEMS = (
    ('Home', '/'),
    ('Archives', '/archives/index.html'),
    ('Categories', '/categories.html'),
    ('Tags', '/tags.html'),
)

# Footer links
LINKS = (
    ('Pelican', 'https://getpelican.com/'),
    ('Python.org', 'https://www.python.org/'),
    ('OpenAI', 'https://openai.com/'),
)

FOOTER_TEXT = 'Powered by AI and Pelican.'

# AI Blog Configuration
AI_BLOG_CONFIG = {
    'show_reading_time': True,
    'show_categories': True,
    'show_tags': True,
    'show_social_share': True,
    'max_related_posts': 3,
    'google_analytics': None,  # Disable for testing
} 