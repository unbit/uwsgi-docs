import sys, os
extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'uWSGI'
copyright = u'2012-2014, uWSGI'
version = '2.0'
release = '2.0'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['_static']
htmlhelp_basename = 'uWSGIdoc'
latex_elements = {}
latex_documents = [('index', 'uWSGI.tex', u'uWSGI Documentation', u'uWSGI', 'manual'),]
man_pages = [('index', 'uwsgi', u'uWSGI Documentation', [u'uWSGI'], 1)]
texinfo_documents = [('index', 'uWSGI', u'uWSGI Documentation', u'uWSGI', 'uWSGI', 'The uWSGI application server.', 'Miscellaneous'),]
