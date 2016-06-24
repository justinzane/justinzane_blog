#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

LOAD_CONTENT_CACHE = False

#----- Site Info
AUTHOR = 'Justin [Zane] Chudgar'
SITENAME = 'justinzane'
SITEURL = 'file:///home/justin/syncthing/docs/justinzane_blog/output'
RELATIVE_URLS = True
# DATE_FORMATS = {'en_US': '%Y-%m-%d', }
# LOCALE = 'en_US'
TIMEZONE = 'America/Los_Angeles'

#----- Defaults
DEFAULT_CATEGORY = 'misc'
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_LANG = 'en'
# DEFAULT_METADATA (())     The default metadata you want to use for all articles and pages.
DEFAULT_PAGINATION = 10

#----- Feeds
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_DOMAIN = SITEURL
FEED_MAX_ITEMS = 10
TRANSLATION_FEED_ATOM = None

#----- Blogroll
LINKS = [('**Arch**', 'https://wiki.archlinux.org/index.php/The_Arch_Way'),
         ('Pelican', 'http://getpelican.com/'),
         ('PyMarkdown', 'http://pythonhosted.org/Markdown/extensions/index.html'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('Sheldon Brown', 'http://www.sheldonbrown.com/'),
         ('Ken Rockwell Photography', 'http://www.kenrockwell.com/index.htm'),
         ('KEH Cameras', 'http://www.keh.com/'),
         ('PopeHat', 'http://www.popehat.com/'),
         ]

#----- Social widget
SOCIAL = [('GitHub', 'https://github.com/justinzane'),
          ('Facebook', 'http://www.facebook.com/justinchudgar'), ]

#----- Paths
# ARTICLE_DIR = ''
# ARTICLE_EXCLUDES = ['pages', ]
# FILENAME_METADATA ('(?P<date>\d{4}-\d{2}-\d{2}).*')     
#	The regexp that will be used to extract any metadata from the filename. All 
#	named groups that are matched will be set in the metadata object. The 
#	default value will only extract the date from the filename. For example, if 
#	you would like to extract both the date and the slug, you could set something
#   like: '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'.
DELETE_OUTPUT_DIRECTORY = True
MARKUP = ('rst', 'md',)
OUTPUT_PATH = 'output/'
PAGE_PATHS = ['pages',]
PATH = 'content/'
# PATH_METADATA ('')
#   Like FILENAME_METADATA, but parsed from a page’s full path relative to
#   the content source directory.
# PAGE_EXCLUDES (())
#   A list of directories to exclude when looking for pages.
USE_FOLDER_AS_CATEGORY = True

#----- Tag Cloud
TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100

#----- Processing Options
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
IGNORE_FILES = ['.#*']
NEWEST_FIRST_ARCHIVES = True
OUTPUT_SOURCES = False
# OUTPUT_SOURCES_EXTENSION = '.txt'
PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = False
SUMMARY_MAX_LENGTH = 50
TYPOGRIFY = False

# Take advantage of the following defaults
# STATIC_SAVE_AS = '{path}'
# STATIC_URL = '{path}'
# Replaces: FILES_TO_COPY = (('robots.txt', 'robots.txt'),)
STATIC_PATHS = [
    'extra/robots.txt',
    'images',
]
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
}

#----- Plugins --------------------------------------------------------------------
PLUGIN_PATHS = ['plugins',]
PLUGINS = ['albums',
#           'gzip_cache',
		   'neighbors',
		   'related_posts',
		   'sitemap',
		   'pelican_albums',
#		   'disqus_static',
		   ]
		   
#----- albums
ALBUM_PATH = u'galleries'
THUMBNAIL_OUTPUT_PATH = u'galleries/{slug}/thumbnails'
THUMBNAIL_OUTPUT_FORMAT = u'JPEG'
THUMBNAIL_DEFAULT_SIZE = u'96x96'
THUMBNAIL_DEFAULT_QUALITY = 80
ALBUM_SAVE_AS = u'galleries/{slug}.html'
ALBUM_URL = u'galleries/{slug}.html'
IMAGE_SAVE_AS = u'galleries/{slug}.html'
IMAGE_URL = u'galleries/{slug}.html'
#----- Discus
DISQUS_SITENAME = u'justinzane'
DISQUS_SECRET_KEY = u'0fo3fvZXFsZqt75mywsF7WzYtC1VIRrMQiXMTZysS9tnfuxHx6nWlMPlrjcYa1vH'
DISQUS_PUBLIC_KEY = u'Xlmynh3kr5QOGPSZ9UjYaLWBaqaq2WCJxrFM6lak3BqnHVKXSH8sxL1hc777xW6y'
#----- Google Analytics
GOOGLE_ANALYTICS = "UA-2357728-2"
GOOGLE_ADSENSE_ID = "pub-317407888633431"
#----- Related-posts
RELATED_POSTS_MAX = 5
#----- Sitemap
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
#----- END Plugins -----------------------------------------------------------------

#----- Themes
THEME = 'themes/darkweight'
# THEME_STATIC_PATHS = ['static', ]
# CSS_FILE = 'main.css'

#----- Templates
# JINJA_EXTENSIONS ([])     A list of any Jinja2 extensions you want to use.
# JINJA_FILTERS ({})
#   A list of custom Jinja2 filters you want to use. The dictionary should
#   map the filtername to the filter function. 
#       For example: {'urlencode': urlencode_filter}
#   See Jinja custom filters documentation.
# TEMPLATE_PAGES = {}
# DIRECT_TEMPLATES (('index', 'tags', 'categories', 'archives'))
#   List of templates that are used directly to render content. Typically 
#   direct templates are used to generate index pages for collections 
#   of content (e.g. tags and category index pages).
# PAGINATED_DIRECT_TEMPLATES (('index',))
#   Provides the direct templates that should be paginated.
# EXTRA_TEMPLATES_PATHS ([])
#   A list of paths you want Jinja2 to search for templates. Can be used 
#   to separate templates from the theme. Example: projects, resume, 
#   profile ... These templates need to use DIRECT_TEMPLATES setting.

#-----------------------------------------
#	mdx-attr-cols	mdx-audio		mdx-callouts
#	mdx-customspanclass
#	mdx-del-ins		mdx-embedly		mdx-environment
#	mdx-foldouts	mdx-linkify		mdx-outline
#	mdx-semanticwikilinks			mdx-showable
#	mdx-smartypants mdx-textalign	mdx-titlecase
#	mdx-twitchmoticons				
#	mdx-video
# 	abbr			attr_list		def_list
#   headerid		nl2br			smart_strong
#	smarty			tables			wikilinks

MD_EXTENSIONS = (['admonition', 
                  'codehilite',
				  'collapse',
                  'extra',
                  'cite',
                  'fenced_code',
                  'footnotes',
                  'meta',
                  'picture',
                  'sections',
                  'semanticdata',
                  'semanticwikilinks',
                  'sane_lists',
                  'tables',
                  'text-align',
                  'titlecase',
                  'toc',
                  'twitter'])
#       http://pythonhosted.org/Markdown/extensions/index.html
# ASCIIDOC_OPTIONS ([])     A list of options to pass to AsciiDoc. See the manpage

