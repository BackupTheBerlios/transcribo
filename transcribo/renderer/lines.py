
from frames import BuildingBlock
from content import ref_re, target_re
from transcribo import logger
class Line(BuildingBlock):
    def __init__(self, text, width, number, parent,  align = 'left', refs = None, targets = None, page_break = 0):
    
        BuildingBlock.__init__(self, parent) # parent is the frame the line belongs to.
        self.raw_text = text # text may contain unresolved ref markers. Hence we call it raw text for now.
        self.width = width
        self.number = number # counter for lines within a frame. Used to get the y pos.
        self.align = align
        self.refs = refs # list of references.
        self.targets = targets # list of targets
        self.text = '' # to store the text after resolving the refs
        # page_break: semantics of values:
        # 0: let Paginator do whatever it sees fit
        # 1: make hard page_break before this line
        # 2: make hard page break before this line
        # if it would otherwise be the last on current page.
        # This is to avoid widows and orphans.
        self.page_break = page_break
        
        
    def __len__(self):
        if not self.text:
            text = self.render()
        return len(text)
        
    def receive_page_num(self, page_num):
        '''\
        Propagate the page number string to any targets.
        '''
        for t in self.targets:
            t.set_property(page_num = page_num)

        
    def render(self, resolve = True):
        '''\
        return  the content of the line as unicode string.
        If the line contains a reference marker,
        the line can only be rendered properly if all references are resolved.
        Note that unresolved
        references are unresolved only because the
        page number has been missing so far.
        '''
        
        # Try to resolve any references
        i = 0
        if resolve:
            while i < len(self.refs):
                ref_text = self.refs[i].render()
                if ref_text: # reference is resolved, replace the marker
                    markers = ref_re.finditer(self.text)
                    # get the span of the first reference marker found
                    left = markers[0].start()
                    right = markers.end()
                    self.text[start:end] = ref_text
                    self.refs.pop(i)
                else: # unresolved reference, so keep it for later.
                    i +=1
                    # handle unresolved refs here.
                    # the len method is a problem as it is called vera early in content.py to get the auto width of a frame.

        # alignment
        if self.align == 'right':
            self.text = self.text.rjust(self.width)
        elif self.align == 'center':
             self.text = self.text.center(self.width)
             if isinstance(self.text, str): logger.info('line is a string %s' % self.text)
        return self.text

    def __repr__(self):
        result = 'x:'
        if hasattr(self, 'x'): result += str(self.x)
        else: result += '?'
        result += ', y:'
        if hasattr(self, 'y'): result += str(self.y)
        else: result += '?'
        return ' '.join((result, self.raw_text))


    def get_x(self):
        if  self.calc_x:
            self.x = self.parent.get_x()
            self.calc_x = False
        return self.x
        
        
    def get_y(self):
        if self.calc_y:
            self.y = self.parent.get_y() + self.number
            self.calc_y = False
        return self.y

        
        
    def __cmp__(self, b):
        if self.get_y() < b.get_y(): return -1
        elif self.get_y() > b.get_y(): return 1
        elif self.get_x() < b.get_x(): return -1
        elif self.get_x() > b.get_x(): return 1
        else: return 0
        
        
        
        