

__all__ = ['frames', 'content', 'pages', 'translators',
'lines']







class BuildingBlock:

    def __init__(self, parent, add_to_parent = True):
        self.children = []
        self.x_dep = []
        self.y_dep = []
        if isinstance(parent, BuildingBlock) and add_to_parent:
            parent.children.append(self)
        self.parent = parent

        # flags indicating if pos and size need to be (re-)calculated
        self.calc_x = self.calc_y = True




    def notify_dependent(self, dep, flag):
        for f in getattr(self, dep):
            setattr(f, flag, True)
            f.notify_dependent(dep, flag)


    def __add__(self, other):
        return self.children + other

    def __radd__(self, other):
        return other + self.children

    def __iadd__(self, other):
        """Append a node or a list of nodes to `self.children`."""
        if isinstance(other, list):
            self.children.extend(other)
        else:
            self.children.append(other)
        return self

    def append(self, item):
        self.children.append(item)

    def update(self, **args):
        for k,v in args.items():
            setattr(self, k, v)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.children[key]
        else:
            raise TypeError('Argument must be of type int, not %s.' % type(key))


    def __setitem__(self, key, item):
        if isinstance(key, int):
            self.children[key] = item
        else:
            raise TypeError('Argument must be of type int, not %s.' % type(key))


    def __len__(self):
        return len(self.children)



