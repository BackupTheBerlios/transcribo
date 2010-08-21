

"""This module contains the ContentManager class and various content classes
to be passed on to a ContentManager instance. Each leaf frame must have exactly
 one ContentManager instance to render. Each ContentManager stores at least one
content object in its children attribute as list items.
"""



from transcribo import logger
from transcribo.renderer import BuildingBlock
from singleton import get_singleton

import re
ref_re = re.compile(ur"\{r\d+\}")
target_re = re.compile(ur"\{t\d+\}")
ref_targets_re = re.compile(ur"\{[rt]\d\}")
markers_re = re.compile(ur"\{[rtf].\}")

from lines import Line


class ContentManager(BuildingBlock):
    '''Container class for Content objects each of which will be rendered
    separately before rendering them together. A frame may contain either one
    ContentManager or one or more child frames. So a ContentManager renders
    the content of a leaf frame.'''

    def __init__(self, parent,
        wrapper = None, hyphenator = None,
        translator = None, x_align = 'left'):

        BuildingBlock.__init__(self, parent)
        self.wrapper_cfg = wrapper
        self.hyphenator_cfg = hyphenator
        self.translator_cfg = translator
        self.x_align = x_align
        self.render_count = 0

        
        
    def render(self, max_width, width_mode):
        # counting the calls is needed to decide if lines must be
        # deleted from cache in case of multiple rendering due to unresolved references.
        self.render_count += 1 
        
        # Instantiate the wrapper, if any
        if self.wrapper_cfg:
            self.wrapper_cfg['width'] = max_width
            # add optional hyphenator to the wrapper. this is
            # supported by textwrap2 which is part of the PyHyphen hyphenation library.
            if self.hyphenator_cfg:
                self.wrapper_cfg['use_hyphenator'] = self.hyphenator_cfg
            self.wrapper = get_singleton(**self.wrapper_cfg)
        else: self.wrapper = None
        
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
        # containers for all refs and targets whether resolved or not
        self.refs = []
        self.targets = []
        for child in self:
            if isinstance(child, GenericText):
                    tmp = child.render()
            elif isinstance(child, Reference):
                tmp = child.render()
                if not tmp:
                    if child.enabled: # unresolved Reference
                        tmp = u'{r' + unicode(len(self.refs)) + u'}'
                        self.refs.append(child)
                    else: tmp = u''
            elif isinstance(child, Target):
                tmp = u'{t' + unicode(len(self.targets)) + u'}'
                self.targets.append(child)
            raw_content.append(tmp)


        # Translate the frame's content altogether, if required,
        # skipping any placeholders for later substitution.
        if self.translator:
            i = 0
            previous_is_marker = False
            while i < len(raw_content):
                is_marker = markers_re.match(raw_content[i])
                if is_marker and is_marker.group() == raw_content[i]: # only then is it a reference or target marker
                    # check if previous element must be translated
                    if i > 0 and not previous_is_marker:
                        raw_content[i-1] = self.translator.run(raw_content[i-1])
                    previous_is_marker = True # retain this for next iteration
                    i += 1
                else:
                    # normal text:
                    # join with previous text element if any
                    if i == 0: i += 1
                    elif not previous_is_marker:
                        raw_content[i-1] += raw_content[i]
                        raw_content.pop(i)
                    previous_is_marker = False
                    
            # Translate the last text element
            if not previous_is_marker:
                raw_content[-1] = self.translator.run(raw_content[-1])
                    
        # join the translated results to a single string before wrapping it
        raw_content = u''.join(raw_content)
        
        # and wrap it into lines 
        if self.wrapper:
            raw_content = self.wrapper.wrap(raw_content)
        else: raw_content = [raw_content]
        
        # get the relevant width depending on the length of each
        # line and on whether width_mode is fixed or auto. The width is used when rendering each Line instance.
        # Note that due to unresolved references auto width can yield too large results at this stage.
        if width_mode == 'fixed': width = max_width
        else: # it must be 'auto':
            width = max((len(l) for l in raw_content))
        
        # Get the lines cache:
        root = self.parent.parent
        while not hasattr(root, 'cache'): root = root.parent
        cache = root.cache

        # pack the strings into Line objects.
        lrc = len(raw_content)
        for j in range(lrc):
            # check for reference and target markers
            # first, create containers for refs and targets to be passed on to the Lin instances
            cur_refs = []
            cur_targets = []
            # Iterate over any reference and target markers within the line:
            reftargets = ref_targets_re.finditer(raw_content[j])
            for r in reftargets:
                # extract the index of the Reference or Target object
                idx = int(r.group()[2:-1]) # this cuts off '{r' and '}'
                if r.group()[1] == u'r': # it is a reference
                    cur_refs.append(self.refs[idx])
                elif r.group()[1] == u't': # it is a target
                    cur_targets.append(self.targets[idx])
                    # delete the target marker. We do not need it anymore as we have found its Line instance
                    raw_content[j] = raw_content[j].replace(r.group(), u'')
                    
            # generate page break info to be used by the paginator:
            brk = 0 # simplesoft page break if needed
            if (j == 0) or (j == lrc - 2): brk = 2 # avoid widows and orphans
            if j == lrc - 1: last_in_para = True # last line of paragraph should not be block-aligned by Line-render()
            else: last_in_para = False
            
            # Generate and store the Line instance
            cache.append(Line(raw_content[j], width, j,
                self.parent, self.x_align, last_in_para,
                refs = cur_refs, targets = cur_targets,
                page_break = brk))
            
        self.lines = raw_content # is this really needed?
        return (width, len(raw_content))


class GenericText:
    '''Content class for text. '''

    def __init__(self, parent, text = None, translator = None):
        parent += self
        self.text = text
        self.translator_cfg = translator
        if self.translator_cfg:
            self.translator = get_singleton(**self.translator_cfg)
        else:
            self.translator = None
        
    def render(self):
        if self.translator:
            return self.translator.run(self.text)
        else:
            return self.text

class FillChar(GenericText):
    '''\
    Fill a line with a character. It is mainly used for the dotted lines in a table of contents.
    The render method returns a marker that is replaced by lines.Line.render().
    '''
    
    def render(self):
        return u'{f' + self.text + u'}'
    

# Factory functions

def getContentManager(styles, cur, style = ''):
    '''
    return a content.ContentManager instance with the
    specified style (defaults to '').

    'styles: a dictionary with style data
    'cur'': the current frame in which the ContentManager will be placed

    'style': a string of words defining the styles of wrapper, translator and hyphenator.
    Example: style = 'wrapper indent2 translator upper hyphenator en_U'
    The order of the commands in the string does not matter. Separators except for white space are
    not allowed.
    '''


    # Prepare the style string for rudimentary parsing:
    words = style.split()

    # Choose the wrapper
    try:
        i = words.index('wrapper')
        words.pop(i)
        wrapper_name = words.pop(i)
    except ValueError:
        wrapper_name = 'default'

    # Choose the translator
    try:
        i = words.index('translator')
        words.pop(i)
        translator_name = words.pop(i)
    except ValueError:
        translator_name = 'default'


    # Choose the hyphenator
    try:
        i = words.index('hyphenator')
        words.pop(i)
        hyphenator_name = words.pop(i)
    except ValueError:
        hyphenator_name = 'default'

    # Choose x_alignment
    try:
        i = words.index('x_align')
        words.pop(i)
        x_align_name = words.pop(i)
    except ValueError:
        x_align_name = 'default'
        
    if words: raise ValueError('Unknown content style: ' + str(words))

    # Get the corresponding styles
    wrapper_style = styles['wrapper'][wrapper_name]
    translator_style = styles['translator'][translator_name]
    hyphenator_style = styles['hyphenator'][hyphenator_name]
    x_align_style = styles.content[x_align_name]['x_align']

    return ContentManager(parent = cur, wrapper = wrapper_style,
    hyphenator = hyphenator_style,
        translator = translator_style,
        x_align = x_align_style)


class Reference:
    def __init__(self, parent, ref_man, id, property_name = 'page_num'):
        parent += self
        self.id = id
        self.property_name = property_name
        self.target = None
        self.enabled = True
        ref_man.add_ref(self)

    def __repr__(self):
        result = u'<transcribo.renderer.Reference instance. id: %s; target: %s' % (unicode(self.id), unicode(self.target))
        r = self.render()
        if r: result += u'resolved as %s' % r
        else: result += u'unresolved.'
        return result
        
    def render(self):
        if self.target:
            result = self.target.get_property(self.property_name)
        else: result = None
        return result


class Target:
    def __init__(self, parent, ref_man, id, **properties):
            if parent: parent += self
            self.id = id
            self.properties = {}
            self.set_property(**properties)
            ref_man.add_target(self)


    def __repr__(self):
        return u'<transcribo.renderer.content.target instance. id: %s, page_num: %s' %(unicode(self.id), unicode(self.properties['page_num']))
        
        
    def set_property(self, **kwargs):
        self.properties.update(kwargs)

    def get_property(self, name):
        return self.properties[name]

class RefManager:
    def __init__(self):
        self.refs = {}
        self.targets = {}
        

    def add_ref(self, r):
        if r.id in self.refs:
            self.refs[r.id] = tuple(list(self.refs[r.id]).append(r))
        else:
            self.refs[r.id] = (r,)
        if r.id in self.targets:
            r.target = self.targets[r.id]

    def add_target(self, target):
        for i in target.id:
            self.targets[i] = target
            # resolve related references
            if i in self.refs:
                for r in self.refs[i]:
                    r.target = target
                    
                    
    def disable_unresolved(self):
        for id in self.refs:
            for r in self.refs[id]:
                if not r.render():
                    r.enabled = False
