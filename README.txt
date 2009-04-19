

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
used. rst2txt roughly maps the nodes of the Docutils doctree to Frame instances.

Note: Currently, rst2txt is heavily under construction. Do not use it at this stage.
To see the renderer at work, run the test script in the test/ subdirectory.



1.2 The renderer
-------------------------

The renderer is the core of Transcribo. It is premised on an almost
complete abstraction of layout and content.

*   The key concept to achieve simple yet
    powerful layout capabilities is the Frame class. Each Frame instance represents a
    rectangular area within the final output. Its position and size are determined dynamically
    relative to other frames during the rendering process. Frames can be nested.
    The RootFrame instance controls the rendering process and assembles the line
    snippits rendered by each frame to form complete text lines. This allows
    things like multiple columns, nested enumerations etc. In future versions,
    the RootFrame will also control pagination features.
    
*   Content: Leafs of the tree of Frame instances store the actual content, i.e. text,
    mathematical expressions, MusicXML etc. Currently, only GenericText is supported.
    More precisely, each leaf Frame must have a ContentManager instance which controls the
    rendering of the content it contains. Each content element is rendered separately.
    A special feature is the possibility to attach a translator instance to each
    content object as well as to the ContentManager. This feature is required,
    in particular, for Braille translation. The ContentManager is also responsible
    for wrapping and hyphenating the content, if required.
    
All aforementioned features are highly configurable through dictionaries passed to the
constructors. Future versions should support configuration through JSON files.
    
    
2. the Frame API
======================

(to be completed; meanwhile please see the documented sources and the test.py script)


3. The ContentManager API
==============================

(to be completed; meanwhile please see the documented sources and the test.py script)

