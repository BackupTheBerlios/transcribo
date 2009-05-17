"""Base classes for references and targets.
References are resolved as early as possible,
i.e. when instantiating a new reference or target.
A reference is resolved if and only if its render attribute is not None. The render attribute is then identical to the target's render method.
References whose id attribute is None have no target, i.e. they have
to provide their render method themselves. This can be interpreted as self-reference.
A typical use for self-references might be page-numbers.

There is no checking for unresolved references. This must be done by
the other components such as the input parser.
"""






refs = []
targets = []



class Reference:
    '''Base class for references.'''

    def __init__(self, id = None):
        if id:
            partner = [t for t in targets if t.id == id]
            if partner:
                self.render = partner[0].render
                targets.remove(partner[0])
            else:
                self.render = None
                self.id = id
                refs.append(self)
            

class Target:
    '''Base class for target instances.'''

    def __init__(self, id):
        partner = [r for r in refs if r.id == id]
        if partner:
            partner[0].render = self.render
            refs.remove(partner[0])
        else:
            self.id = id
            targets.append(self)
            
            
            
    def render(self):
        '''Override in subclasses.'''
        raise NotImplementedError
        


