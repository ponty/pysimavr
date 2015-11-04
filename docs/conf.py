# import logging
# import sphinx
import sys
import os
try:
    # python 3.3+
    from unittest.mock import MagicMock
except ImportError:
    from mock import Mock as MagicMock

project = 'pysimavr'
author = 'ponty'
copyright = '2011, ponty'

__version__ = None
exec(open(os.path.join('..', project, 'about.py')).read())
release = __version__

# logging.basicConfig(level=logging.DEBUG)
sys.path.insert(0, os.path.abspath('..'))

# Extension
extensions = [
    # -*-Extensions: -*-
    'sphinx.ext.autodoc',
#     'sphinxcontrib.programoutput',
#     'sphinxcontrib.programscreenshot',
#     'sphinxcontrib.gtkwave',
    #     'sphinx.ext.graphviz',
#     'sphinxcontrib.autorun',
    #'sphinx.ext.autosummary',
    #     'sphinx.ext.intersphinx',
]
# intersphinx_mapping = {'http://docs.python.org/': None}

# Source
master_doc = 'index'
templates_path = ['_templates']
source_suffix = '.rst'
exclude_trees = []
pygments_style = 'sphinx'

# html build settings
html_theme = 'default'
html_static_path = ['_static']

# htmlhelp settings
htmlhelp_basename = '%sdoc' % project

# latex build settings
latex_documents = [
    ('index', '%s.tex' % project, u'%s Documentation' % project,
     author, 'manual'),
]

# remove blank pages from pdf
# http://groups.google.com/group/sphinx-
# dev/browse_thread/thread/9_ac_input2e19267d095412d/d60dcba483c6b13d
latex_font_size = '10pt,oneside'

latex_elements = dict(
    papersize='a4paper',
)


# http://read-the-docs.readthedocs.org/en/latest/faq.html
class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
            return Mock()

MOCK_MODULES = ['_ac_input','_hd44780','_inverter','_ledrow','_sgm7','_simavr']
# MOCK_MODULES = ['pysimavr.swig.' + m for m in MOCK_MODULES]
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

