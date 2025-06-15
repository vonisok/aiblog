#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
import logging
sys.path.append(os.curdir)
from pelicanconf import *

# Production URL - Update with your actual domain
SITEURL = 'https://🔸{NetlifySiteID}.netlify.app'
RELATIVE_URLS = False

# Production Feed Settings
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TAG_FEED_ATOM = 'feeds/tag/{slug}.atom.xml'

# JSON Feed for modern feed readers
FEED_ALL_JSON = 'feeds/all.json'

# Social Media Settings
SOCIAL = (
    ('GitHub', '🔸{GITHUB_REPO}'),
    ('RSS', f'{SITEURL}/feeds/all.atom.xml'),
    ('JSON Feed', f'{SITEURL}/feeds/all.json'),
)

# Performance Optimization
DELETE_OUTPUT_DIRECTORY = True
CACHE_CONTENT = True
LOAD_CONTENT_CACHE = True
GZIP_CACHE = True

# Analytics and Monetization
GOOGLE_ANALYTICS = '🔸{GA_TRACKING_ID}'
GOOGLE_ADSENSE = '🔸{ADSENSE_ID}'

# SEO Enhancements for Production
AI_BLOG_CONFIG.update({
    'google_analytics': '🔸{GA_TRACKING_ID}',
    'google_adsense': '🔸{ADSENSE_ID}',
    'enable_json_feed': True,
    'enable_amp': False,  # Can be enabled later
    'enable_pwa': True,   # Progressive Web App features
})

# Social Media Meta Tags
SOCIAL_META = {
    'twitter_card': 'summary_large_image',
    'twitter_site': '🔸{TWITTER_USERNAME}',
    'twitter_creator': '🔸{TWITTER_USERNAME}',
    'og_locale': 'en_US',
    'og_type': 'website',
    'og_site_name': SITENAME,
}

# Production Plugins
PLUGINS.extend([
    'json_feed',
    'optimize_images',
    'gzip_cache',
])

# Image Optimization
OPTIMIZE_IMAGES = True
OPTIMIZE_IMAGES_RESPONSIVE_SIZES = [300, 600, 900, 1200]
OPTIMIZE_IMAGES_QUALITY = 85

# Security Headers (for Netlify _headers file)
SECURITY_HEADERS = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://pagead2.googlesyndication.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://www.google-analytics.com;",
}

# Netlify Specific Settings
NETLIFY_CMS = False  # Can be enabled for content management
NETLIFY_BUILD_HOOK = '🔸{NETLIFY_BUILD_HOOK}'

# Production URL Structure (no trailing slashes)
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'

# Sitemap for Production
SITEMAP.update({
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
        'indexes': 0.6,
        'pages': 0.4
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'daily',
        'pages': 'monthly'
    },
    'exclude': ['tag/', 'category/', 'author/']
})

# Robots.txt for Production
ROBOTS_TXT_TEMPLATE = '''User-agent: *
Allow: /

Sitemap: {siteurl}/sitemap.xml

# Block AI crawlers if needed
# User-agent: GPTBot
# Disallow: /
'''.format(siteurl=SITEURL)

# Production Caching
CACHE_PATH = '.cache'
CONTENT_CACHING_LAYER = 'generator'

# Minification (if plugin available)
MINIFY = {
    'remove_comments': True,
    'remove_empty_space': True,
    'remove_all_empty_space': False,
    'reduce_boolean_attributes': True,
    'remove_optional_attribute_quotes': False,
}

# Static File Optimization
STATIC_PATHS.extend([
    'extra/_headers',
    'extra/_redirects',
    'extra/manifest.json',
])

EXTRA_PATH_METADATA.update({
    'extra/_headers': {'path': '_headers'},
    'extra/_redirects': {'path': '_redirects'},
    'extra/manifest.json': {'path': 'manifest.json'},
})

# Production Debug Settings
DEBUG = False
LOG_FILTER = [(logging.WARN, 'TAG_SAVE_AS')]

# Performance Monitoring
PERFORMANCE_BUDGET = {
    'javascript': 100,  # KB
    'css': 50,         # KB
    'images': 500,     # KB per page
    'fonts': 100,      # KB
}

# CDN Settings (if using)
CDN_URL = ''  # Can be configured for assets

# Backup and Recovery
BACKUP_ENABLED = True
BACKUP_FREQUENCY = 'daily'

# Version for cache busting
import hashlib
import time
CACHE_BUSTER = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]

# Custom Production Variables
CUSTOM_VARS.update({
    'environment': 'production',
    'build_time': time.strftime('%Y-%m-%d %H:%M:%S UTC'),
    'cache_buster': CACHE_BUSTER,
})

# Content Delivery Network
if CDN_URL:
    STATIC_URL = CDN_URL
    FEED_DOMAIN = CDN_URL

# Production Template Settings
JINJA_ENVIRONMENT.update({
    'auto_reload': False,
    'cache_size': 1000,
})

# Article Limits for Performance
MAX_ARTICLES_ON_INDEX = 10
MAX_ARTICLES_IN_FEED = 20

# Production Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'pelican.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
} 