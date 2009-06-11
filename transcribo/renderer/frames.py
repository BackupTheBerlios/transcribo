# Transcribo - a library to convert various document formats into plain text


from transcribo import logger



class RenderingError(Exception):
    pass



class LineStorageError(RenderingError):
    pass
        
        
class BuildingBlock:

    def __init__(self, parent):
        self.children = []
        self.x_dep = []
        self.y_dep = []
        if isinstance(parent, BuildingBlock):
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
       
       
       
            
class Frame(BuildingBlock):
    '''Represents a rectangular area within the rendered document.

    '''

    def __init__(self, parent,
        x_anchor = None, x_hook = '', x_align = '',
        x_offset = 0, right_indent = 0,
        y_anchor = None, y_hook = '', y_align = '',
        y_offset = 0, lines_below = 0,
        max_width = 0, width_mode = 'auto',
        max_height = 0, height_mode = 'auto'):

        BuildingBlock.__init__(self, parent)

        # initialization
        self.lines = 0

        # horizontal position
        self.x_anchor = x_anchor # the frame whose x position will be used
        x_anchor.x_dep.append(self)
        self.x_hook = x_hook # the anchor frame's part to draw on (left, right, center)
        self.x_align = x_align # the part of self to align with the hook (left, right, center)
        self.x_offset = x_offset # absolute offset relative to the hook etc.
        self.right_indent = right_indent
        
        # vertical position
        self.y_anchor = y_anchor
        y_anchor.y_dep.append(self)
        self.y_hook = y_hook
        self.y_align = y_align
        self.y_offset = y_offset

        # width
        self.max_width =  max_width
        self.width_mode = width_mode # 'fixed' or 'auto', i.e. the content determines the width
        
        # height
        self.max_height = max_height
        self.height_mode = height_mode
        self.lines_below = lines_below
        
        
            
        
    def get_x(self):
        '''return the absolute horizontal position of the frame's left column'''
        # need to calculate?
        if self.calc_x:
            self.x = self.x_anchor.get_x()
            if self.x_align == 'left':
                self.x += self.x_offset
                # x_anchor.right_indent is ignored here above.
                # Meaningful? Use max. of both instead?

            elif self.x_align == 'right':
                self.x -= self.width - self.right_indent
            elif self.x_align == 'center':
                self.x -= self.width // 2
                # left- and right_indent are ignored here above. Meaningful?

            if self.x_hook == 'right':
                self.x += self.x_anchor.width
            elif self.x_hook == 'center':
                self.x += self.x_anchor.width // 2
                
                self.notify_dependent('x_dep', 'calc_x')
            self.calc_x = False
        return self.x


    def get_y(self):
        '''return the absolute vertical position of the frame's upper line'''

        # need to calculate?
        if self.calc_y:
            self.y = self.y_anchor.get_y()
            if self.y_align == 'top':
                self.y += self.y_offset
            elif self.y_align == 'bottom':
                self.y -= self.height - self.lines_below
            elif self.y_align == 'center':
                self.y -= self.height // 2 # handled y_offset etc.
                    # correctly?
                    
            if self.y_hook == 'bottom':
                self.y += self.y_anchor.height
            elif self.y_hook == 'center':
                self.y += self.y_anchor.height // 2
                
            self.notify_dependent('y_dep', 'calc_y')
            self.calc_y = False
        return self.y



    def render(self):
        '''render the frame's content or its child frames' content '''

        if not self.children:
            raise RenderingError, 'Nothing to render.'

        if not self.max_width:
            self.max_width = self.parent.max_width - self.x_offset - self.right_indent
            if self.x_anchor is not self.parent:
                if self.x_hook == self.x_align == 'left':
                    self.max_width -= (self.x_anchor.get_x() - self.parent.get_x())
                elif self.x_hook == 'right' and self.x_align == 'left':
                    self.max_width -= (self.x_anchor.get_x() +
                        self.x_anchor.width - self.parent.get_x())
                else: raise RenderingError('Calculation of max_width not implemented for x_hook = %s, x_align = %s.'
                    % (self.x_hook, self.x_align))
                

            
     # render any content
        if not isinstance(self[0], Frame):
            # render the content frame and store the number of lines.
            # the ContentManager will store the lines in the cache
            # The paginator will then operate on the cache.
            (self.width, self.height) = self[0].render(self.max_width,
                self.width_mode)
            
            
        # render subframes
        else:
            for child in self:
                child.render()
                
            # calculate width
            if self.width_mode == 'fixed': self.width = self.max_width
            else:
                self.x = 0
                self.calc_x = False
                self.notify_dependent('x_dep', 'calc_x')
                self.width = max((f.x() + f.width for f in self))
                self.calc_x = True
                self.notify_dependent('x_dep', 'calc_x')

            # calculate height
            if self.height_mode == 'fixed': self.height = self.max_height # what, if lines are too many?
            else: # must be auto. So count the lines.
                self.y = 0
                self.calc_y = False
                self.notify_dependent('y_dep', 'calc_y')
                self.height = max((f.get_y() + f.height for f in self))
                self.calc_y = True
                self.notify_dependent('y_dep', 'calc_y')

                



class RootFrame(BuildingBlock):
    '''Ancestor of all frames. Its render method generates the final output from the
    rendered children. The RootFrame has just children and no content.
    Future versions may add pagination, footnotes etc.'''
    
    def __init__(self, max_width = 60):

        BuildingBlock.__init__(self, None)
        self.width = self.max_width = max_width
        self.cache = []


    def get_x(self):
        return 0

    def get_y(self):
        return 0




    def render(self):
        for c in self.children: c.render()
        return self.cache.sort()



