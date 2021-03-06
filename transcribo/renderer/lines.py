
from transcribo.renderer import BuildingBlock
from content import ref_re, target_re
from transcribo import logger
import re
fillchar_re = re.compile(ur'\{f.\}')
space_re = re.compile(ur'\S\s+\S')


class Line(BuildingBlock):
    def __init__(self, text, width, number, parent,  align = 'left', last_in_para = False, refs = None, targets = None, pager = None):
    
        BuildingBlock.__init__(self, parent, add_to_parent = False) # parent is the frame the line belongs to.
        self.raw_text = text # text may contain unresolved ref markers. Hence we call it raw text for now.
        self.width = width
        self.number = number # counter for lines within a frame. Used to get the y pos.
        self.align = align
        self.refs = refs # list of references.
        self.targets = targets # list of targets
        self.text = '' # to store the text after resolving the refs
        self.pager = pager
        self.last_in_para = last_in_para # avoid block alignment of last line in paragraph
        
        
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
        text = self.raw_text
        # Try to resolve any references
        if resolve:
            markers = ref_re.findall(text)
            i = 0
            for r in self.refs:
                if r.enabled:
                    ref_text = r.render()
                    if ref_text: # reference is resolved, replace the marker
                        text = text.replace(markers[i], ref_text)
                        i += 1
                    else: # unresolved reference, so keep it for later.
                        i += 1
                        # handle unresolved refs here.
                        # the len method is a problem as it is called vera early in content.py to get the auto width of a frame.
                        
                        
        # FillChar markers:
        match = fillchar_re.search(text)
        if match:
            # calculate number of chars to be inserted. 4 is the length of the fillchar marker: e.g. "{fX}"
            l = self.width - len(text) + 4
            c = match.group()[2] # char to use
            text = text.replace(match.group(), c * l)

        # alignment
        if self.align == 'right':
            text = text.rjust(self.width)
        elif self.align == 'center':
             text = text.center(self.width)
        elif self.align == 'block' and (not self.last_in_para):
            delta = self.width - len(text)
            matches = [i for i in space_re.finditer(text)]
            l = len(matches)
            if l: # any spaces found that can be expanded?
                q = float(delta) / l
                if q >= 1:
                    z = int(q)
                    spaces = u' ' * z
                    for i in range(l):
                        m = matches[i]
                        text = spaces.join((text[:m.end() - 1], text[m.end() - 1:]))
                        matches = [j for j in space_re.finditer(text)]
                        delta -= z
                if delta: # so 0 < q < 1
                    p = float(l) / delta
                    for i in range(delta):
                        m = matches[int(i * p)]
                        text = u' '.join((text[:m.end() - 1], text[m.end() - 1:]))
                        matches = [j for j in space_re.finditer(text)]
                
        self.text = text
        return text

    def __repr__(self):
        result = 'x:'
        if hasattr(self, 'x'): result += str(self.x)
        else: result += '?'
        result += ', y:'
        if hasattr(self, 'y'): result += str(self.y)
        else: result += '?'
        result = unicode(result)
        return u' '.join((result, self.raw_text))


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
        
        
        
        