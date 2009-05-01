


class Line:
    def __init__(self, elements):
        self.elements = elements
        
    def __len__(self):
        return sum((len(e) for e in self.elements))
        
    def __str__(self):
        return ''.join((str(e) for e in self.elements))
        
        
        