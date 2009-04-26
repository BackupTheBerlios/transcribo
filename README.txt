

Transcribo - a plain text rendering library written in Python
=================================================================

Project home: http://transcribo.berlios.de/

Mercurial repository: http://hg.berlios.de/repos/transcribo/

Mailing-List: transcribo-dev@berlios.de

Version: 0.1 (experimental)

Author: Dr. Leo <dr-leo@users.berlios.de>

License: GPL (http://www.opensource.org/licenses/gpl-license.html)

(c) 2009 Dr. leo




1. Introduction
=================

Transcribo is a pure Python library to render input from various sources as plain unicode text. It currently
consists of two subpackages:

1.1 rst2txt
--------------

In combination with the renderer, this will be a Writer component for Docutils (http://docutils.sourceforge.net/).
Once finished, it will allow to render
reStructuredText files as plain text. At the same time it demonstrates how the renderer (see below) can be
used. rst2txt roughly maps the nodes of the Docutils doctree to Frame instances that form a fram tree. However, the frame tree
has a somewhat different structure than the docutils doc tree as frames do not
necessarily reflect the document structure. E.g., sections are not rendered as parent frames of the section content,
but at the same level.

The rst2txt package is heavily under construction. Currently, the following
node types are supported:

document, title, section, paragraph, text, bullet_list, enumerated_list, list_item


1.2 The renderer
-------------------------

The renderer is the core of Transcribo. It is premised on an almost
complete abstraction of layout and content.

*   The key concept to achieve simple yet
    powerful layout capabilities is the Frame class. Each Frame instance represents a
    rectangular area within the final output. Its position and size are determined dynamically
    relative to other frames during the rendering process. Frames can be nested.
    The RootFrame instance controls the rendering process and assembles the line
    snippets rendered by each frame to form complete text lines. This allows
    things like multiple columns, nested enumerations etc. In future versions,
    the RootFrame will also control pagination features.
    
*   Content: Leafs of the tree of Frame instances store the actual content within a
    content.ContentManager instance which, in turn, may store various content elements such as
    text, mathematical expressions, MusicXML etc. Currently, only GenericText is supported.
    More precisely, each leaf Frame must have a ContentManager instance which controls the
    rendering of the content it contains. Each content element is rendered separately.
    A special feature is the possibility to attach a translator instance to each
    content object as well as to the ContentManager. This feature is required,
    in particular, for Braille translation. The ContentManager is also responsible
    for wrapping and hyphenating the content, if required.
    
All aforementioned features are highly configurable through dictionaries passed to the
constructors. 
    
    
2. the Frame API
======================

(to be completed; meanwhile please see the documented sources and the test.py script)


3. The ContentManager API
==============================

(to be completed; meanwhile please see the documented sources and the test.py script)



4. Testing
==============

The tst subdirectory contains two test scripts that should work out of the box:

* test.py: demonstrates the renderer API by rendering a nested enumeration.
* rst2txt.py is a command line tool. A demo text file shows some of the features of the rst2txt writer.



5. Contributing
==================

Development is in an early stage. Any help is very much appreciated. Feel free to join the mailing
list, check out the Mercurial repository and start coding, 

