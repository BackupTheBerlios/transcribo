
from transcribo.renderer.frames import BuildingBlock


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
        
    def render(self):
        if self.text: return self.text
        if self.refs:
            self.text = self.raw_text.format((r.render() for r in self.refs))
        else:
            self.text = self.raw_text
        # alignment
        if self.align == 'right':
            self.text = self.text.rjust(self.width)
        elif self.align == 'center':
             self.text = self.text.center(self.width)
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
        
        
        
        