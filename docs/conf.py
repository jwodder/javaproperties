from   __future__ import unicode_literals
import os.path
import sys

sys.path.insert(0, os.path.abspath('..'))
import javaproperties
from   javaproperties import __version__

project   = 'javaproperties'
author    = 'John T. Wodder II'
copyright = '2016 John T. Wodder II'

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

autodoc_default_flags = ['members', 'undoc-members']
# NOTE: Do not set 'inherited-members', as it will cause all of the
# MutableMapping methods to be listed under `Properties`.
#autodoc_member_order = 'bysource'

intersphinx_mapping = {
    'https://docs.python.org/': None,
    "python2": ("https://docs.python.org/2", None),
}

templates_path = ['_templates']
exclude_patterns = ['_build']
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
master_doc = 'index'
version = __version__
release = __version__
today_fmt = '%Y %b %d'
default_role = 'py:obj'
pygments_style = 'sphinx'
todo_include_todos = True

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_last_updated_fmt = '%Y %b %d'
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #'preamble': '',

    # Latex figure (float) alignment
    #'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, project + '.tex', project + ' Documentation', author, 'manual')
]

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, project, project + ' Documentation', [author], 3)
]
man_show_urls = True
