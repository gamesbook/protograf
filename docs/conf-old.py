# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'protograf'
copyright = '2016-2025, Derek Richard Hohls'
author = 'Derek Hohls'
version = release = '0.1.0'

# -- General configuration ------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

exclude_patterns = [
    'build',
    'dist',
    'Thumbs.db',
    '.DS_Store',
]
extensions = []
language = 'en'
master_doc = 'index'
pygments_style = 'sphinx'
source_suffix = '.rst'
# templates_path = ['_templates']

# -- Options for HTML output ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
