Transcribo -

a plain text rendering library written in Python



Version: 0.1

Author: Dr. Leo <fhaxbox66 <at> googlemail.com>

License: GPL 3.0

(c) 2009 Dr. leo




Introduction
=============

...


2. Frames
==========

Positioning frames
---------------------------


A frame's position can be determined relative to any other frame. Assume a simple
one-column text with headings and paragraphs. All frames are children
of the root frame which prescribes the maximum width.

The horizontal position of all frames will be determined relative to the root frame.
To achieve this, we instantiate each frame with the following arguments:
    x_from = parent
        width_from = parent
        
    We alter the left margin for each frame using the left_margin argument.
    
    The vertical position of the first frame (usually a heading) is derived from the root frame:
    
        y_from = parent
        
Further, we want each subsequent frame begin at the line following the last line
of the preceeding one:

y_from = preceeding_frame



    
    
    


frames will be determined relative to the root frame.
