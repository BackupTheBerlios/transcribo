from transcribo import logger
from transcribo.renderer import BuildingBlock
from lines import Line
from singleton import get_singleton

"""This module contains the ContentManager class and various content classes
to be passed on to a ContentManager instance. Each leaf frame must have exactly
one ContentManager instance to render. Each ContentManager stores at least one
content object in its children attribute as list items.
"""


class ContentManager(BuildingBlock):
    '''Container class for Content objects each of which will be rendered
    separately before rendering them together. A frame may contain either one
    ContentManager or one or more child frames. So a ContentManager renders
    the content of a leaf frame.'''

    def __init__(self,
        wrapper = {'module_name': 'textwrap', 'class_name': 'TextWrapper'},
        translator = None, x_align = 'left'):

        BuildingBlock.__init__(self)
        self.wrapper_cfg = wrapper
        self.translator_cfg = translator
        self.x_align = x_align
        
        

    def render(self, width):
        # Instantiate the wrapper. This is obligatory.
        self.wrapper_cfg['width'] = width
        self.wrapper = get_singleton(**self.wrapper_cfg)
        
        # instantiate the optional translator. Note that each element may have
        # its own translator. However, the content manager's translator
        # works on the entire content rather than on each element.
        
        if self.translator_cfg:
            self.translator = get_singleton(**self.translator_cfg)
        else:
            self.translator = None
            
        # Render each element and puth the results together. Future versions
        # may need to handle other content types.
        concat_children = ''.join([e.render()  for e in self])
        
        # Translate the frame's content altogether, if required
        if self.translator: concat_children = self.translator.run(concat_children)
        
        # and wrap it using the wrapper instance. Hyphenation can be implemented using
        # PyHyphen and textwrap2. But by default, the textwrap standard module is used.
        wrapped = self.wrapper.wrap(concat_children)
        
        # alignment
        if self.x_align == 'right':
            for i in range(len(wrapped)): wrapped[i] = wrapped[i].rjust(width)
        elif self.x_align == 'center':
            for i in range(len(wrapped)): wrapped[i] = wrapped[i].center(width)
            
        # pack the strings into Line objects. Future versions will
        # handle non-string content such as references, inline-commands etc.
        result = [Line(w) for w in wrapped]
        return result


class GenericText:
    '''Content class for text. '''

    def __init__(self, text = None, translator = None, **args):
        self.text = text
        self.translator_cfg = translator
        for k,v in args:
            setattr(self, k, v)
        if self.translator_cfg:
            self.translator = get_singleton(**self.translator_cfg)
        else:
            self.translator = None
        
    def render(self):
        if self.translator:
            return self.translator.run(self.text)
        else:
            return self.text

        