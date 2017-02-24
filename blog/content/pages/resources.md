Title: Resources
Date: 2016-11-10 10:20
Modified: 2016-11-10 18:40
Tags: resources, documentation
Category: info
Slug: resources
Authors: Chris Holdgraf
Summary: A collection of resources that we've found useful in improving our documentation

Below we'll keep a semi-updated list of resources that we've found useful in writing and improving our own documentation. If you've got a suggestion for something else to add, please add it as a comment on our github issue on this [here](https://github.com/BIDS/docathon/issues/5).

# Table of Contents

1. [Documentation tools](#documentation-tools)
2. [Guides and articles on technical communication](#guides-comm)
3. [Events and resources for holding events](#events)

# Documentation tools <a name="documentation-tools"></a>
---
These cover tools and software that are useful in documentation. If you have a suggestion for a new tool, add a comment [here](https://github.com/BIDS/docathon/issues/4).

## Python

### numpydoc

[numpydoc](https://pypi.python.org/pypi/numpydoc) is a set of extension for
sphinx initially used by the numpy project and now more widely used in the
scientific ecosystem. Among other features, it provides extra sphinx directives, and
understands the numpy docstring syntax. This allows you to quickly build websites for your project.

### Napoleon

[Sphinxcontrib-napoleon](https://pypi.python.org/pypi/sphinxcontrib-napoleon)
is a set of extensions for Sphinx which understand both NumPy and Google style
docstrings.

### Doctr

[Doctr](https://github.com/drdoctr/doctr) is meant to simplify the deployment
of documentation from Travis-CI to GitHub pages, by providing a single tool to
setup, build and deploy documentation builds. 

It is an alternative to readthedocs, which is sometimes difficult in getting dependencies installed.

Doctr is still young and could have many features contributed, maybe by you! 

### Sphinx Gallery 

[Sphinx Gallery](https://github.com/sphinx-gallery/sphinx-gallery) is a Sphinx
extension that will automatically generate a gallery from a repository of
examples that generate matplotlib plots. It also auto-generates a jupyter notebook that can be downloaded from the html page in the docs.

Sphinx Gallery automatically makes all identifiers present in every code block
link to their definition. In conjunction with [intersphinx] this is allows
seamless navigation between related projects. 

### custom_inherit

[custom_inherit](https://github.com/meowklaski/custom_inherit) is a Python package that provides convenient, light-weight tools for inheriting/merging docstrings in customizeable ways. This helps facilitate thorough and consistent documentation - documentation need not be duplicated manually when docstring sections are being inherited.

It provides both a decorator and a metaclass for facilitating docstring inheritance/merging. Numpy, Google, & reST docstring styles are supported out of the box.

### Documentation portals


The following tools fall under the category of "Documentation portals" they attempt
to gather documentation from several sources in a coherent, uniform and
searchable portal. 

[Devdocs](http://devdocs.io/) started as a portal to gather documentation for
javascript projects. Now it has expanded to many projects and languages. It's browser-based but stores content locally so available online projects can opt-in and write a
"Scrapper" to parse already existing HTML docs.

It does _not_ have a concept of "next/previous" pages so is not meant for read-through
tutorials.

[Dash](https://kapeli.com/dash) is a similar project. It is (for now)
available for MacOS only, as native application. You can use it to get online
resources, but is mostly meant to work off-line.

[PyDoc](https://pydoc.io) fills again a similar niche.  PyDoc first version
were made public at end of 2016. Unlike the two above, PyDoc is meant to be
Python only, and has no intent to be available off-line. Its tight integration
with Python should allows it to automatically build _api only_ docs for all
Python project on PyPI and Warehouse. 


### Miscellaneous documentation tools   


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


# Guides and articles on technical communication <a name="guides-comm"></a>
---

These are resources for communicating clearly, particularly about technical matters. If you have a suggestion for a new resource, add a comment [here](https://github.com/BIDS/docathon/issues/5)

## Articles
* Modern Physics' Guide to Writing Well - <https://drive.google.com/file/d/0B8VZ4vaOYWZ3ZDJzcWNWVUFFR00/view?usp=sharing>

## Web posts
* <https://www.elsevier.com/connect/infographic-tips-to-writing-better-science-papers>
* <https://jacobian.org/writing/great-documentation/>
* <https://emptysqua.re/blog/write-an-excellent-programming-blog/>
* <https://emptysqua.re/blog/resources-for-writing-about-programming/>

## Videos
* <https://www.pycon.fr/2016/videos/lire-ecrire-la-doc.html>


# Events and resources for holding events <a name="events"></a>
---

There are also many events that follow the same principles as the Docathon. We've compiled a list of them below. If you have a new event to suggest, post a comment [here](https://github.com/BIDS/docathon/issues/19)

## Hackathon Events / Orgs
* [Hacktoberfest](https://hacktoberfest.digitalocean.com/)
* [24PullRequests](https://24pullrequests.com/)
* [Code Curiosity](https://codecuriosity.org/)
* [National Novel Writing Month](http://nanowrimo.org/)
* [Julython](http://www.julython.org/)

## Documentation Events / Orgs
* [Write the Docs](http://www.writethedocs.org/) (they also have a "writing day" event, [here](http://www.writethedocs.org/conf/na/2015/writing-day/#projects) is a link to their projects page)
* [The Open News Code Convening for docs on OSS](https://source.opennews.org/en-US/articles/building-guide-open-sourcing-newsroom-code/)
* Open Stack doc day [here](https://www.openstack.org/blog/2011/04/dedicated-doc-day/) and [here](https://wiki.openstack.org/wiki/Documentation/DocDay)
* [Atlassian documentation day](http://blogs.atlassian.com/2010/03/the_atlassian_doc_sprint_was_awesome/)

## Guides / How-To
* [How to plan a doc sprint](https://ffeathers.wordpress.com/2012/09/07/how-to-plan-a-doc-sprint/)
* [Learning from a doc sprint](https://ffeathers.wordpress.com/2016/01/17/learnings-from-a-doc-sprint/)
* [Doc bug fixits](https://ffeathers.wordpress.com/2016/07/08/doc-bug-fixits-a-doc-sprint-to-fix-issues/)
* [A twitter thread about docs/sprints](https://twitter.com/ericholscher/status/821429334879584256) 
