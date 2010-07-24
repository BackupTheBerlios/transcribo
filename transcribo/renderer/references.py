class Reference:
    def __init__(self, id, property_name = 'page_num'):
        self.id = id
        self.property_name = property_name
        self.target = None
        
    def resolve(self):
        if self.target and self.property_name in self.target:
            return self.target[self.property_name]
        else:
            return None
        

class Target(dict):
    def __init__(self, id, **properties):
        self.id = id
        self.update(properties)
        
        

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
