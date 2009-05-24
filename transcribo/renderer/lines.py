


class Line:
    def __init__(self, text, width, number, frame, alignn = 'left', refs = None):
        self.raw_text = text
        self.wicth = width
            self.number = number
        self.frame = frame
        self.alignn = alignn
        self.refs = refs
        
    def __len__(self):
        return len(self.str(text))
        
    def __str__(self):
        if self.refs:
            self.text = self.raw_text.format((r.render() for r in self.refs))
        else:
            self.text = self.raw_text
        # alignnment
        if self.align == 'left':
            self.text = self.text.ljust(self.width)
        elif self.align == 'right':
            self.text = self.text.rjust(self.width)
        elif self.align == 'center':
             self.text = self.text.center(self.width)
        return self.text

    def x(self):
        return self.frame.x()
        
    def y(self):
        return self.frame.y() + self.number
        
    def __cmp__(self, a, b):
        if a.y() < b.y(): return -1
        elif a.y() > b.y(): return 1
        elif a.x() < b.x(): return -1
        elif a.x() > b.x(): return 1
        else: return 0
        
        
        
        