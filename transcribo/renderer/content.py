

"""This module contains the ContentManager class and various content classes
to be passed on to a ContentManager instance. Each leaf frame must have exactly
 one ContentManager instance to render. Each ContentManager stores at least one
content object in its children attribute as list items.
"""



from transcribo import logger
from transcribo.renderer.frames import BuildingBlock
from lines import Line
from singleton import get_singleton
from references import Reference, Target




class ContentManager(BuildingBlock):
    '''Container class for Content objects each of which will be rendered
    separately before rendering them together. A frame may contain either one
    ContentManager or one or more child frames. So a ContentManager renders
    the content of a leaf frame.'''

    def __init__(self, parent,
        wrapper = None,
        translator = None, x_align = 'left'):

        BuildingBlock.__init__(self, parent)
        self.wrapper_cfg = wrapper
        self.translator_cfg = translator
        self.x_align = x_align
        self.render_count = 0
        self.lines = []

        
        
    def render(self, max_width, width_mode):
        self.render_count += 1 # count number of calls of render for efficiency reasons.
        
        # Instantiate the wrapper. This is obligatory.
        self.wrapper_cfg['width'] = max_width
        self.wrapper = get_singleton(**self.wrapper_cfg)
        
        # instantiate the optional translator. Note that each element may have
        # its own translator. However, the content manager's translator
        # works on the entire content rather than separately on each element.
        
        if self.translator_cfg:
            self.translator = get_singleton(**self.translator_cfg)
        else:
            self.translator = None
            
        # Render each element and put the results together. Future versions
        # may need to handle other content types.
        raw_content = []
        refs = []
        count = 0
        for child in self:
            tmp = child.render()
            if isinstance(tmp, basestring):
                raw_content.append(tmp)
                
            # unresolved references have returned themselves rather than a string:
            # a placeholder will be inserted instead and the reference instances will be
            # stored separately to be rendered finally upon pagination.
            else:
                refs.append(tmp)
                raw_content.append(str(count).join(('\{', '}')))
                count += 1


        # Translate the frame's content altogether, if required,
        # skipping any placeholders for later substitution.
        if self.translator:
            for i in range(len(raw_content)):
                if not raw_content[i].startswith('\}'):
                    raw_content[i] = self.translator.run(raw_content[i])
        
        raw_content = ''.join(raw_content)
        
        # and wrap it using the wrapper instance. Hyphenation can be implemented using
        # PyHyphen and textwrap2. But by default, the textwrap standard module is used.
        raw_content = self.wrapper.wrap(raw_content)
        
        # get the relevant width depending on the length of each
        # line and on whether width_mode is fixed or auto. The width is used when rendering each Line instance.
        if width_mode == 'fixed': width = max_width
        else: # it must be 'auto':
            width = max((len(l) for l in raw_content))
        
        
        # Get the lines cache:
        root = self.parent.parent
        while not hasattr(root, 'cache'): root = root.parent
        cache = root.cache

        # in case this frame has already been rendered, remove the lines from the cache.
        if self.render_count > 1:
            i=0
            while i < len(cache):
                if cache[i].parent == self: cache.pop(i)
                else: i += 1
            
        # pack the strings into Line objects. Future versions will
        # handle non-string content such as references, inline-commands etc.
        for j in range(len(raw_content)):
            # Handle references
            c = raw_content[j].count('\{')
            r = refs[:c]
            cache.append(Line(raw_content[j], width, j,
                self.parent, self.x_align, refs = r))
            refs[:c] = []
        self.lines = raw_content # is this really needed?
        return (width, len(raw_content))


class GenericText:
    '''Content class for text. '''

    def __init__(self, parent, text = None, translator = None, **args):
        parent += self
        self.text = text
        self.translator_cfg = translator
        for k,v in args.items():
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

