

Transcribo - a plain text rendering library written in pure Python
======================================================================

Project home: http://transcribo.berlios.de/

Mercurial repository: http://hg.berlios.de/repos/transcribo/

Mailing-List: transcribo-dev@berlios.de

Version: 0.1 (experimental)

Author: Dr. Leo <dr-leo@users.berlios.de>

License: GPL (http://www.opensource.org/licenses/gpl-license.html)

(c) 2009 Dr. leo




1. Introduction
=================

    
The transcribo project is aimed at the development of 
a modular, easy to use and powerful cross-platform software to convert various file formats
to well-formatted plain text. What might seem a somewhat strange goal in the age of pdf and HTML turns out to
be very useful, e.g., for output devices which can only handle plain text such as Braille
printers. Indeed, Transcribo has been designed with the objective in mind to allow printing
documents in high-quality Braille. However, Transcribo should be useful in all
contexts where plain text in complex layouts is needed.

The heart of transcribo is the renderer package. It is the back-end of the whole conversion tool chain.
Frontends specific to the supported input formats
parse the input file, derive the layout structure and call the renderer to generate (i) a proprietary
tree-like representation of the document, and (ii) traverse the tree creating a line-by-line representation.
Thereafter, the renderer's paginator
is called to insert page breaks. create headers and footers etc. Finally, the paginated line-by-line
representation is assembled to a plain text file.

The renderer allows to attach to each content block (paragraph, heading, reference etc.) a
specific translator to perform translations on the text. In combination with
frontends for mark-up languages, this
feature allows the user to control the output at a very high level of granularity.

Currently the only frontend parses a subset of reStructuredText including sections, paragraphs,
multi-level lists and enumerations. A second frontend for plain text input is being prepared.




2. System requirements and installation
==============================

Transcribo is developed on Python 2.6. It should run on older versions, possibly with
small changes. There are no dependencies. However, if you want to
use the translation features for Braille, you may wish to install a Braille translator such as
liblouis or YABT. In addition, if you want to use the frontend for reStructuredText,
you will need Docutils, because the frontend for reStructuredText is nothing but a docutils
writer component. Use the rst2txt.py script in the test directory to translate rST documents.

Transcribo is a pure Python package. It is installed by unpacking the archive and typing
from the shell prompt something like:

cd <package dir>

python setup.py install

Then run one of the scripts in the test/ subdirectory

