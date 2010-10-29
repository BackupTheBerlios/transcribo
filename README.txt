
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

.. contents ::

.. sectnum::



What's new?
==================

*Version 0.7*

This is a milestone release with many new features. Much of the code has been refactored.

    * unified command line front end using argparse (dependency under Python2.6)
    * new generic configuration system named yaconfig with cascading style sheets using PyYAML (new dependency)

      * supports multiple YAML files which are successively mixed into a tree of nested dictionaries
      * multiple inheritance from any node specified by absolute or local paths (relative paths not fully supported)
      * supports string interpolation similar to configparser from the stdlib (this feature is not used though)

    * more rST features including

      * references and targets (not yet footnotes)
      * table of contents with or without page numbers
      * definition lists
      * transitions
      * rST reader (the module that reads rST files using Docutils; it is essentially a Docutils writer component!)
        is fully configurable through cascading style sheets in YAML format;
        this means that the Docutils own configuration system is no longer visible to the Transcribo user.

    * no longer depends on a Braille translator such as YABT
    * hard page breaks improved; can be used with rST reader through style sheets: break page after end of section etc.


*Version 0.6*

* hard page breaks
* avoid widows and orphans when soft-breaking pages
* support for Hyphenation (requires PyHyphen, see the installation instructions below)
* numerous bug fixes and improvements

*Version 0.5.3:*

This is a minor bug fix release.


Introduction
=================

The transcribo project is aimed at the development of 
a modular, easy to use and powerful cross-platform software to convert various file formats
into accurate plain text. What might seem a somewhat strange goal in the age of pdf and HTML turns out to
be very useful, e.g., for output devices which can only handle plain text such as Braille
embossers. Indeed, Transcribo has been designed with the objective in mind to allow printing
documents in high-quality Braille. However, Transcribo should be useful in all
contexts where text-based output formats in highly customizable layouts are needed.

Transcribo has been designed so as to separate the processing of the input file from the actual rendering
algorithm. Hence, there are two layers: In the input layer various format-specific readers parse the input streams and feed
them into the renderer (second layer).

More specifically, the input layer may contain readers specific to
each supported  input format. readers do the following:

* parse the input file,
* derive from it the layout structure and
* use the renderer to generate

  + a proprietary tree representation of the document, and
  + traverse the tree creating a line-by-line representation of the document.

* Thereafter, the renderer's paginator
  is called to insert white space as margins, page breaks, create headers and footers, resolve page references  etc.
* Finally, the paginated line-by-line
  representation is assembled to a plain text file.

The renderer allows to attach to each content block (paragraph, heading, reference etc.) a
specific *translator* and *wrapper including optional hyphenation* to perform translations and achieve the required text outline. In combination with
readers for mark-up languages, this
feature allows the user to control the output at a high level of granularity.

Currently there are readers for `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ and plain text. Additional readers
for formats such as LaTeX, ODF, RTF, XML formats such as DocBook and HTML appear useful.

Installation and usage
=====================================

Transcribo is developed with Python 2.6. It should run on older versions, possibly with
small changes. There are a few mandatory and optional dependencies:

* `PyYAML <http://pypi.python.org/pypi/PyYAML>`_ 
* `argparse <http://pypi.python.org/pypi/argparse>`_
  It is already included in the stdlib of Python 2.7.
* if you want to have hyphenated output, you'll need `PyHyphen <http://pypi.python.org/pypi/PyHyphen/>`_
* If you want to
  use the translation features for Braille, you may wish to install a Braille translator such as
  `liblouis <http://liblouis.googlecode.com>`_ or `YABT <http://pypi.python.org/pypi/YABT>`_.
* `Docutils <http://docutils.sourceforge.net>`_, because Transcribo's rST reader is essentially a docutils
  writer component. Well, if you are happy with txt2txt, forget this.

Transcribo is a pure Python package. It is installed by unpacking the archive and typing
from the shell prompt something like: ::

    cd <package dir>
    python setup.py install

The test/test.py script demonstrates how to use Transcribo programmatically.
Use the *transcribo.py* script from the shell prompt to generate paginated plain text from
rST or plain text documents. Type 'transcribo.py --help' to read an argparse-generated help text
on the available commands. Examples::

    # Generate a block-aligned text with en_US hyphenation dictionary. Requires PyHyphen!
    transcribo infile.rst outfile.out --styles align-block hyphen_en_US
    # Note that '--reader rst' is used by default. the 'base.yaml' style file is
    # loaded automatically.
    # Generate paginatd plain text from plain text. Each blank line
    # is interpreted as a paragraph separator.
    transcribo infile.txt outfile.out --reader plaintext --styles align-block


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