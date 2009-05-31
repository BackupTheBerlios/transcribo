


class Line:
    def __init__(self, text, width, number, frame, align = 'left', refs = None, targets = None):
        self.raw_text = text
        self.width = width
        self.number = number
        self.frame = frame
        self.align = align
        self.refs = refs
        self.targets = targets
        
    def __len__(self):
        return len(self.__str__())
        
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
        
    def __cmp__(self, b):
        if self.y() < b.y(): return -1
        elif self.y() > b.y(): return 1
        elif self.x() < b.x(): return -1
        elif self.x() > b.x(): return 1
        else: return 0
        
        
        
        