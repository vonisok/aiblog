#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import os
from datetime import datetime

# Basic Settings
AUTHOR = '🔸{BlogName}'
SITENAME = '🔸{BlogName}'
SITEURL = ''  # For development
SITESUBTITLE = 'Fresh insights, generated daily.'

PATH = 'content'
OUTPUT_PATH = 'output'

TIMEZONE = 'UTC'
DEFAULT_LANG = 'en'

# Theme and Appearance
THEME = 'themes/aiblog'
THEME_STATIC_DIR = 'theme'
CSS_FILE = 'main.css'

# Content Settings
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# Archive Settings
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

# Category and Tag Settings
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

# Author Settings (single author blog)
AUTHOR_SAVE_AS = ''  # Disable author pages
AUTHORS_SAVE_AS = ''

# Article Settings
DEFAULT_CATEGORY = 'Tech News'
USE_FOLDER_AS_CATEGORY = False
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = True

# Summary Settings
SUMMARY_MAX_LENGTH = 50  # Number of words in summary

# Feed Settings
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (
    ('GitHub', '🔸{GITHUB_REPO}'),
    ('RSS', '/feeds/all.atom.xml'),
)

# Blogroll
LINKS = (
    ('Pelican', 'https://getpelican.com/'),
    ('Python.org', 'https://www.python.org/'),
    ('OpenAI', 'https://openai.com/'),
)

# Pagination
DEFAULT_PAGINATION = 10
PAGINATION_PATTERNS = (
    (1, '{name}{extension}', '{name}{extension}'),
    (2, '{name}{number}{extension}', '{name}{number}{extension}'),
)

# URL Settings
RELATIVE_URLS = True

# Static Paths
STATIC_PATHS = [
    'images',
    'extra/robots.txt',
    'extra/favicon.ico',
    'extra/CNAME',
]

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
}

# Plugin Settings
PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'sitemap',
    'seo',
    'readtime',
    'neighbors',
]

# Sitemap Plugin Settings
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
        'indexes': 0.5,
        'pages': 0.3
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# SEO Settings
SEO_REPORT = True
SEO_ENHANCER = True
SEO_ENHANCER_OPEN_GRAPH = True
SEO_ENHANCER_TWITTER_CARDS = True

# Custom Settings for AI Blog
AI_BLOG_CONFIG = {
    'show_reading_time': True,
    'show_categories': True,
    'show_tags': True,
    'show_social_share': True,
    'enable_dark_mode': True,
    'enable_search': True,
    'enable_comments': False,  # Can be enabled later with Disqus
    'google_analytics': '🔸{GA_TRACKING_ID}',
    'google_adsense': '🔸{ADSENSE_ID}',
    'max_related_posts': 3,
}

# Development Settings
DELETE_OUTPUT_DIRECTORY = True
LOAD_CONTENT_CACHE = False

# Markdown Extensions
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {
            'permalink': True,
            'title': 'Table of Contents'
        },
    },
    'output_format': 'html5',
}

# Date Format
DEFAULT_DATE_FORMAT = '%B %d, %Y'
DATE_FORMATS = {
    'en': '%B %d, %Y',
}

# Cache Settings
CACHE_CONTENT = False
CACHE_PATH = '.cache'
GZIP_CACHE = True

# Output Settings
WRITE_SELECTED = []
OUTPUT_RETENTION = []

# Template Settings
JINJA_ENVIRONMENT = {
    'trim_blocks': True,
    'lstrip_blocks': True,
}

# Menu Settings
MENUITEMS = (
    ('Home', '/'),
    ('Archives', '/archives.html'),
    ('Categories', '/categories.html'),
    ('Tags', '/tags.html'),
)

# Custom Variables for Templates
CUSTOM_VARS = {
    'current_year': datetime.now().year,
    'site_description': 'AI-powered blog delivering fresh insights on technology and productivity.',
    'meta_keywords': 'AI, technology, productivity, automation, web development, machine learning',
    'twitter_username': '🔸{TWITTER_USERNAME}',
    'github_username': '🔸{GITHUB_USERNAME}',
}

# Performance Settings
CACHE_CONTENT = True
CHECK_MODIFIED_METHOD = 'mtime'
CONTENT_CACHING_LAYER = 'reader'

# Locale Settings
LOCALE = ['en_US.UTF-8']

# Typogrify Settings (if plugin is available)
TYPOGRIFY = True

# Article Order
ARTICLE_ORDER_BY = 'date'
DEFAULT_ORPHANS = 0
DEFAULT_PAGINATION = 10

# Debug Settings
DEBUG = True
LOG_FILTER = []

# Template Pages
TEMPLATE_PAGES = {
    'extra/sitemap.xml': 'sitemap.xml',
}

# Direct Templates
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'archives']
PAGINATED_TEMPLATES = {'index': None, 'tag': None, 'category': None, 'author': None}

# Featured Articles (if needed)
FEATURED_TAGS = ['featured', 'popular', 'trending']

# Footer Settings
FOOTER_TEXT = f"© {datetime.now().year} 🔸{{BlogName}}. Powered by AI and Pelican." 