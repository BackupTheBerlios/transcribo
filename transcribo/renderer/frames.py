# Transcribo - a library to convert various document formats into plain text


from transcribo import logger
from lines import Line
from renderer import environment as env



class RenderingError(Exception):
    pass



class LineStorageError(RenderingError):
    pass
        
        
class BuildingBlock:
    def __init__(self):
        self.children = []

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

    def __init__(self, parent = None,
        x_anchor = None, x_hook = '', x_align = '',
        x_offset = 0, right_indent = 0,
        y_anchor = None, y_hook = '', y_align = '',
        y_offset = 0, lines_below = 0,
        max_width = 0, width_mode = 'auto',
        max_height = 0, height_mode = 'auto'):

        BuildingBlock.__init__(self)
        self.parent = parent

        # initialization
        self.children = []
        parent += self
        self.lines = []

        # horizontal position
        self.x_anchor = x_anchor # the frame whose x position will be used
        self.x_hook = x_hook # the anchor frame's part to draw on (left, right, center)
        self.x_align = x_align # the part of self to align with the hook (left, right, center)
        self.x_offset = x_offset # absolute offset relative to the hook etc.
        self.right_indent = right_indent
        
        # vertical position
        self.y_anchor = y_anchor
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
        

        
    def x(self):
        '''return the absolute horizontal position of the frame's left column'''
        result = self.x_anchor.x()
        if self.x_align == 'left':
            result = result + self.x_offset # x_anchor.right_indent is ignored here. Meaningful? Use max. of both instead?
        elif self.x_align == 'right':
            result = result - self.width() - self.right_indent
        elif self.x_align == 'center':
            result = result - self.width() // 2 # left- and right_indent are ignored here. Meaningful?
        if self.x_hook == 'left': pass # this could be omitted, but it's more clear.
        elif self.x_hook == 'right':
            result = result + self.x_anchor.width()
        elif self.x_hook == 'center':
            result += self.x_anchor.width() // 2
        return result

            

    def y(self):
        '''return the absolute vertical position of the frame's upper line'''
        result = self.y_anchor.y()
        if self.y_align == 'top':
            result = result + self.y_offset
        elif self.y_align == 'bottom':
            result = result - self.height() - self.lines_below
        elif self.y_align == 'center':
            result = result - self.height() // 2 # left- and right_indent are ignored here. Meaningful?
        if self.y_hook == 'top': # this could be omitted, but it's more clear.
            pass
        elif self.y_hook == 'bottom':
            result = result + self.y_anchor.height()
        elif y_hook == 'center':
            result = result + self.y_anchor.height() // 2
        return result

        
    def height(self):
        '''return the actual frame height'''
        if self.height_mode == 'fixed':
            return self.max_height
        if self.lines:
            return self.lines + self.lines_below
        else:
            return max([(c.y() - self.y() + c.height()) for c in self.children]) + self.lines_below
            
            
    def get_max_width(self):
        result = self.parent.width() - (self.x() - self.parent.x()) - self.right_indent
        return result


    def width(self):
        '''return the actual width of the frame'''
        if self.width_mode == 'fixed':
            if self.max_width:
                return self.max_width
            else: 
                return self.get_max_width()
        # so width_mode must be auto, so take the width of the content or the biggest child frame
        elif self.lines:
            return max([len(l) for l in self.lines])
        elif isinstance(self[0], Frame):
            return             max([(child.x() - self.x() + child.width()) for child in self])
        else:
            raise FrameError('Cannot calculate width.')


    def render(self):
        '''render the frame's content or its child frames' content and store it
        as a list of lines.Line instances in self.lines.'''

        if not self.children:
            raise RenderingError, 'Nothing to render.'

 
        if not self.max_width:
            self.max_width = self.get_max_width()
            
     # render any content
        if not isinstance(self[0], Frame):
            # render the content frame and store the number of lines.
            # the lines themselves will be sent to the cache automatically.
            self.lines = self[0].render(width = self.max_width)
            logger.debug('Rendered lines %s ... %s' % (self.lines[0], self.lines[-1]))
            
            
        # render any children
        else:
            for child in self:
                child.render()



class RootFrame(BuildingBlock):
    '''Ancestor of all frames. Its render method generates the final output from the
    rendered children. The RootFrame has just children and no content.
    Future versions may add pagination, footnotes etc.'''
    
    def __init__(self, max_width = 60, paginator = None):

        BuildingBlock.__init__(self)
        self.max_width = max_width
        self.paginator = paginator
        self.cache = []


    def x(self):
        return 0

    def y(self):
        return 0

    def height(self):
        return 0 # any height allowed

    def width(self):
        if self.paginator:
            return self.paginator.get_width()
        else:
            return self.max_width

    def store(self, content, x, y):
        # add blank lines, if cache is too small to store current line.
        while len(self.cache) - 1 < y: self.cache.append([u''])
        
        # check if line is already too long to store the new content.
        if sum((len(piece) for piece in self.cache[y])) > x:
            raise LineStorageError('Line in cache is too long. (content = %s; length = %d, x = %d, y = %d)'
            % (self.cache[y], len(self.cache[y]), x, y))
        content.ljust(x)
# rework this!!!


    def get_physical_line_number(self, n):
        '''return physical line number given the paginator settings.'''
        
    

    def assemble(self, frame):
        for c in frame.children:
            if isinstance(c, Frame): self.assemble(c)
        x = frame.x()
        y = frame.y()
        count = y
        for l in frame.lines:
            # handle page refs here. If necessary, re-render the whole frame with
            # known page numbers.
            self.get_physical_line_number(count)
            self.store(l, x, count)
            count += 1


    def render(self):
        for c in self.children: c.render()
        for c in self.children: self.assemble(c)
        return '\n'.join(self.cache)



