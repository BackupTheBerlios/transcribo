


class Line:
    def __init__(self, text, commands = None, ref = [], targets = []):
        self.text= text
        self.commands = commands
        self.ref = ref
        self.targets = targets
    
    def __len__(self):
        return len(self.text)
        
        