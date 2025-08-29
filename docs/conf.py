# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

project = 'Python Guide'
copyright = '2025, Viswamedha Nalabotu'
author = 'Viswamedha Nalabotu'

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.autosummary",]

templates_path = ['_templates']
exclude_patterns = []
autosummary_generate = True

html_theme = 'furo'
html_static_path = ['_static']
