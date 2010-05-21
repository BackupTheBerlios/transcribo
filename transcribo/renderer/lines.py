
from transcribo.renderer.frames import BuildingBlock


class Line(BuildingBlock):
    def __init__(self, text, width, number, parent,  align = 'left', refs = None, targets = None, page_break = 0):
    
        BuildingBlock.__init__(self, parent)
        self.raw_text = text
        self.width = width
        self.number = number
        self.align = align
        self.refs = refs
        self.targets = targets
        self.text = ''
        # page_break: semantics of values:
        # 0: let Paginator do whatever it sees fit
        # 1: make hard page_break before this line
        # 2: make hard page break before this line
        # if it would otherwise be the last on current page.
        # This is to avoid widows and orphans.
        self.page_break = page_break
        
        
    def __len__(self):
        if not self.result:
            self.result = self.__str__()
        return len(self.result)
        
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

    def __str__(self):
        result = 'x:'
        if hasattr(self, 'x'): result += str(self.x)
        else: result += '?'
        result += ', y:'
        if hasattr(self, 'y'): result += str(self.y)
        else: result += '?'
        return ' '.join(result, self.raw_text)


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
        
        
        
        