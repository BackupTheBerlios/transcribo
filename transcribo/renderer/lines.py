


class Line:
    def __init__(self, text, width, home, alignn = 'left', refs = None):
        self.raw_text = text
        self.wicth = width
        self.home = home
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

        
        
        