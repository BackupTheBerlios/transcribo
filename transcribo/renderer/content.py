

"""This module contains the ContentManager class and various content classes
to be passed on to a ContentManager instance. Each leaf frame must have exactly
 one ContentManager instance to render. Each ContentManager stores at least one
content object in its children attribute as list items.
"""



from transcribo import logger
from frames import BuildingBlock
from singleton import get_singleton

import re
ref_re = re.compile(ur"\{_r\d+\}")
target_re = re.compile(ur"\{_t\d+\}")
ref_target_re = re.compile(ur"\{_[rt]\d+\}")

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
                if not tmp: # unresolved Reference
                    self.refs.append(child)
                    tmp = u'{_r' + unicode(len(self.refs)) + u'}'
                elif isinstance(child, Target):
                    tmp = u'{_t' + unicode(len(self.targets)) + u'}'
                    self.targets.append(child)
            raw_content.append(tmp)


        # Translate the frame's content altogether, if required,
        # skipping any placeholders for later substitution.
        if self.translator:
            i = 0
            previous_matches = False
            while i < len(raw_content):
                matches = ref_target_re.match(raw_content[i])
                if matches and matches.group() == raw_content[i]: # only then is it a reference or target marker
                    if i > 0:
                        raw_content[i-1] = self.translator.run(raw_content[i-1])
                    i += 1
                    previous_matches = True
                else:
                    # normal text:
                    if not previous_matches and i > 0:
                        raw_content[i-1] += raw_content[i]
                        raw_content.pop(i)
                    else: i += 1
            if not matches:
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


# if this frame has been rendered before, remove its lines from the cache
# as it will be rendered again, e.g. with resolved references.
        if self.render_count > 1:
            i=0
            while i < len(cache):
                if cache[i].parent == self: cache.pop(i)
                else: i += 1
            
        # pack the strings into Line objects. 
        for j in range(len(raw_content)):
            # check for reference and target markers
            # first, create containers for refs and targets to be passed on to the Lin instances
            cur_refs = []
            cur_targets = []
            # Iterate over any reference and target markers within the line:
            reftargets = ref_target_re.finditer(raw_content[j])
            for r in reftargets:
                # extract the index of the Reference or Target object
                idx = int(r.group()[3:-1]) # this cuts off '{_r' and '}'
                if r.group()[2] == 'r': # it is a reference
                    cur_refs.append(self.refs[idx])
                else: # it must be a target
                    cur_targets.append(self.targets[idx])
                    # delete the target marker. We do not need it anymore as we have found its Line instance
                    raw_content[j] = raw_content[j].strip(r.group())
                    

            # generate page break info to be used by the paginator:
            if (j == 0) or (j == len(raw_content) - 2): brk = 2 # avoid widows and orphans
            else: brk = 0 # simple soft page break
            if isinstance(raw_content[j], str):
                logger.info('raw_content is string: %s' % raw_content[j])
            cache.append(Line(raw_content[j], width, j,
                self.parent, self.x_align,
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
    def __init__(self, parent, refman, id, property_name = 'page_num'):
        parent += self
        self.id = id
        self.property_name = property_name
        self.target = None
        refman.add_ref(self)

    def render(self):
        if self.target:
            result = self.target[self.property_name]
        else: result = None
        return result


class Target(dict):
    def __init__(self, parent, refman, id, **properties):
        if parent: parent += self
        self.id = id
        self.set_property(**properties)
        refman.add_target(self)

    def set_property(self, **kwargs):
        self.update(kwargs)



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
            if i in self.refs:
                for r in self.refs[i]:
                    r.target = target
                    
                    
