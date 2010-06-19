
==================================================================
Transcribo - a plain text rendering library written in pure Python
==================================================================

| *Project home:* http://transcribo.berlios.de/
| *Mercurial repository:* http://hg.berlios.de/repos/transcribo/
| *Mailing List:* transcribo-dev@berlios.de
| *Version:* 0.7 alpha
| *Author:* Dr. Leo <dr-leo@users.berlios.de>
| *License:* GPL (http://www.opensource.org/licenses/gpl-license.html)
| (c) 2009-2010 Dr. leo




-----


.. sectnum::



What's new?
==================

*Version 0.7*

* styles are now in YAML format

*Version 0.6*

* hard page breaks
* avoid widows and orphans when soft-breaking pages
* support for Hyphenation (requires PyHyphen, see the installation instructions below)
* numerous bug fixes and improvements

*Version 0.5.3:*

This is a bug fix release.


Introduction
=================

The transcribo project is aimed at the development of 
a modular, easy to use and powerful cross-platform software to convert various file formats
into accurate plain text. What might seem a somewhat strange goal in the age of pdf and HTML turns out to
be very useful, e.g., for output devices which can only handle plain text such as Braille
embossers. Indeed, Transcribo has been designed with the objective in mind to allow printing
documents in high-quality Braille. However, Transcribo should be useful in all
contexts where plain text in complex layouts is needed.

Transcribo has been designed so as to separate the processing of the input file from the actual rendering
algorithm. Hence, there are two layers: In the input layer various format-specific frontends parse the input streams and feed
them into the renderer (second layer).

More specifically, the input layer may contain front ends specific to
each supported  input format. Front ends do the following:

* parse the input file,
* derive from it the layout structure and
* use the renderer to generate

  + a proprietary tree representation of the document, and
  + traverse the tree creating a line-by-line representation of the document.

* Thereafter, the renderer's paginator
  is called to insert white space as margins, page breaks, create headers and footers etc.
* Finally, the paginated line-by-line
  representation is assembled to a plain text file.

The renderer allows to attach to each content block (paragraph, heading, reference etc.) a
specific *translator* and *wrapper including optional hyphenation* to perform translations and achieve the required text outline. In combination with
frontends for mark-up languages, this
feature allows the user to control the output at a very high level of granularity.

Currently there are frontends for .. `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ and plain text. Additional frontends
for formats such as LaTeX, ODF, RTF, XML formats such as DocBook and HTML appear useful.

Installation and usage
=====================================

General
----------------

Transcribo is developed with Python 2.6. It should run on older versions, possibly with
small changes. There are a few dependencies. Well, you can live without, but some functions may not work or require minor
modifications, eg. in the styles module.

* As per version 0.6, Transcribo requires the hyphenation package
  `PyHyphen <http://pypi.python.org/pypi/PyHyphen/>`_
* If you want to
  use the translation features for Braille, you may wish to install a Braille translator such as
  `liblouis <http://liblouis.googlecode.com>`_ or `YABT <http://pypi.python.org/pypi/YABT>`_. In addition,
  if you want to use the frontend for reStructuredText,
  you will need `Docutils <http://docutils.sourceforge.net>`_, because the frontend for reStructuredText is essentially a docutils
  writer component. Use the *transcribo-rst.py* script, a Docutils frontend tool, to generate plain text from rST documents.
  Without Docutils, you can only generate plain text from plain text using the *transcribo-txt.py* script.
  Type python transcribo-txt.py --help to see the command line options.

Transcribo is a pure Python package. It is installed by unpacking the archive and typing
from the shell prompt something like: ::

    cd <package dir>
    python setup.py install

Then run one of the scripts in the scripts/ or test/ subdirectory (see above).

Using the rST frontend
-----------------------

The module transcribo.rST.py is a Docutils writer component. See the Docutils documentation for background info.
It supports a reasonable subset of the rST features. Implemented features include paragraphs, sections,
section numbers (basic support), bullet lists,
enumerations, block quotes, line blocks, references (page references are on the wish list), strong and emphasis
(represented by cappitalized letters), inline literals. To translate an rST document into plain text, use the
transcribo-rst.py frontend tool. Use the command line or the configuration file to modify the page width and the
translator to be used (default is None). All other configurations are contained in ``transcribo.renderer.styles.py``.


Downloading and contributing
===============================

* You can download the latest release_ or a snapshot_ from the Mercurial repository
* if Mercurial_ is installed on your machine, you can pull the latest sources_
* Feel free to join the `mailing list`_
* send an e-mail to the author_ 
* visit the `project page`_ and contribute code, bug reports or feedback
* use it under the terms of the GPL 3.0
* have fun!



.. _Mercurial: http://mercurial.selenic.com/wiki/

.. _Python: http://www.python.org


.. _snapshot: http://hg.berlios.de/repos/transcribo/archive/tip.zip

.. _sources: http://developer.berlios.de/hg/?group_id=10799

.. _project page: http://developer.berlios.de/projects/transcribo

Documentation
=================

Documentation to be built with Sphinx is planned. The renderer's API is illustrated by test/test.py which renders a nested
enumeration. A simple example is provided by transcribo/plaintext.py, the plain text frontend. More complex examples including extensive usage
of styles can be found in rST.py. Please feel free to submit any questions to the mailing list or directly to the author.

.. _mailing list: http://developer.berlios.de/mail/?group_id=10799

.. _author: dr-leo@users.berlios.de

.. _release: http://pypi.python.org/pypi/Transcribo/