Title: Resources
Date: 2016-11-10 10:20
Modified: 2016-11-10 18:40
Tags: resources, documentation
Category: info
Slug: resources
Authors: Chris Holdgraf
Summary: A collection of resources that we've found useful in improving our documentation

Below we'll keep a semi-updated list of resources that we've found useful in writing and improving our own documentation. If you've got a suggestion for something else to add, please add it as a comment to our github issue on this [here](https://github.com/BIDS/docathon/issues/5).

# Learning how to document projects
---

## Articles
* Modern Physics' Guide to Writing Well - https://drive.google.com/file/d/0B8VZ4vaOYWZ3ZDJzcWNWVUFFR00/view?usp=sharing

## Web posts
* https://www.elsevier.com/connect/infographic-tips-to-writing-better-science-papers
* https://jacobian.org/writing/great-documentation/
* https://emptysqua.re/blog/write-an-excellent-programming-blog/
* https://emptysqua.re/blog/resources-for-writing-about-programming/

## Videos
* https://www.pycon.fr/2016/videos/lire-ecrire-la-doc.html

# Documentation tools
---
##Python

### numpydoc

[numpydoc](https://pypi.python.org/pypi/numpydoc) is a set of extension to
sphinx initially used by the numpy project and now more widely used in the
scientific ecosystem. Among other it provide extra sphinx directives, and
understand the numpy docstring syntax.

### Napoleon

[Sphinxcontrib-napoleon](https://pypi.python.org/pypi/sphinxcontrib-napoleon)
is a set of extension for Sphinx which understand both NumPy and Google style
docstrings.

### Doctr

[Doctr](https://github.com/drdoctr/doctr) is meant to simplify the deployment
of documentation from Travis-CI to GitHub pages, by providing a single tool to
setup, build and deploying documentation build. 

It is an alternative to readthedocs where it is not always simple to get all
dependency installed.

Doctr is still young and an easy to contribute project with a number of missing
features. 

### Sphinx Gallery 

[Sphinx Gallery](https://github.com/sphinx-gallery/sphinx-gallery) is a Sphinx
Extensions that will automatically generate a gallery from a repository of
examples.

Sphinx Gallery automatically make all identifiers present in every code block
to link to their definition. In conjunction with [intersphinx] this is allow
seamless navigation in between related projects. 


### Documentation portals


The following tools enter the category of "Documentation portals" they attempt
to gather documentation from several source in a coherent, uniform and
searchable portal. 

[Devdocs](http://devdocs.io/) started as a portal to gather documentation for
javascript only. Now expanded to many project. Browser based but store content
in local storage so available online projects need to opt-in a write a
"Scrapper" to parse already existing HTML docs.

It _not_ have a concept of next-previous page so is not meant for read-through
tutorials.

[Dash](https://kapeli.com/dash) is a similar project. It is though (for now)
available for MacOS only, as native application. It is capable to get online
resources, but is mostly meant to work off-line.

[PyDoc](https://pydoc.io) fills again a similar niche.  PyDoc first version
were made public at end of 2016. Unlike the two above, PyDoc is meant to be
Python only, and has no intent to be available off-line. Its tight integration
with Python should allows it to automatically build _api only_ docs for all
Python project on PyPI and Warehouse. 


### Miscs    


[Docrepr](https://pypi.python.org/pypi/docrepr) extend the concept of
MimeBundle that can be found in IPython and Jupyter to extend it to python's
docstring. Using docrepr, the Jupyter Notebook and Spyder can show docstring of
interactive object using rich html. 


[thebe test](https://github.com/michaelpacer/thebe-test) is a prototype to make
example written using sphinx interactive and backed by an actual running
kernel. Either running on a temporary server in the cloud (like SymPy
documentation console), or even cnnecting to a locally running jupyter notebook
server. 



## C++
- [Doxygen](http://www.stack.nl/~dimitri/doxygen/)
- [BoostBook](http://www.boost.org/doc/libs/1_62_0/doc/html/boostbook.html) and [QuickBook](http://www.boost.org/doc/libs/1_62_0/doc/html/quickbook.html)
- [Breathe](https://breathe.readthedocs.io/en/latest/) for connecting Sphinx and Doxygen
- [cldoc](https://jessevdk.github.io/cldoc/) — clang-based documentation generator
