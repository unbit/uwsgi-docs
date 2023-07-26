import sys, os
extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'uWSGI'
copyright = '2012-2016, uWSGI'
version = '2.0'
release = '2.0'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['_static']
htmlhelp_basename = 'uWSGIdoc'
latex_elements = {}
latex_documents = [('index', 'uWSGI.tex', 'uWSGI Documentation', 'uWSGI', 'manual'),]
man_pages = [('index', 'uwsgi', 'uWSGI Documentation', ['uWSGI'], 1)]
texinfo_documents = [('index', 'uWSGI', 'uWSGI Documentation', 'The uWSGI application server.', 'Miscellaneous'),]
