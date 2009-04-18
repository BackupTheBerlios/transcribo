# Transcribo - a library to convert various document formats into plain text

__all__ = ['core', 'contenttypes', 'lines', 'singleton']

from transcribo import logger
from lines import Line



class RenderingError(Exception):
    def __init__(self, message, *values):
        self.message = message
        self.values = values
        
    def __str__(self):
        s = self.message % self.values
        return repr(s)



class LineStorageError(RenderingError):
    pass
        
        



class Frame:
    '''Represents a rectangular area within the rendered document.

    '''

    def __init__(self, parent = None, content = None,
        x_anchor = None, x_hook = '', x_align = '',
        left_indent = 0, right_indent = 0,
        y_anchor = None, y_hook = '', y_align = '',
        lines_above = 0, lines_below = 0,
        max_width = 0, width_mode = 'auto',
        max_height = 0, height_mode = 'auto'):

        self.parent = parent
        self.content = content

        # initialization
        self.children = []
        parent.children.append(self)
        self.lines = []

        # horizontal position
        self.x_anchor = x_anchor # the frame whose x position will be used
        self.x_hook = x_hook # the anchor frame's part to draw on (left, right, center)
        self.x_align = x_align # the part of self to align with the hook (left, right, center)
        self.left_indent = left_indent # absolute offset relative to the hook etc.
        self.right_indent = right_indent
        
        # vertical position
        self.y_anchor = y_anchor
        self.y_hook = y_hook
        self.y_align = y_align
        self.lines_above = lines_above

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
            result = result + self.left_indent # x_anchor.right_indent is ignored here. Meaningful? Use max. of both instead?
        elif self.x_align == 'right':
            result = result - self.width() - self.right_indent
        elif self.x_align == 'center':
            result = result - self.width() // 2 # left- and right_indent are ignored here. Meaningful?
        if self.x_hook == 'left': pass # this could be omitted, but it's more clear.
        elif self.x_hook == 'right':
            result = result + self.x_anchor.width()
        elif x_hook == 'center':
            result += self.x_anchor.width() // 2
        return result

            

    def y(self):
        '''return the absolute vertical position of the frame's upper line'''
        result = self.y_anchor.y()
        if self.y_align == 'top':
            result = result + self.lines_above
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
            return len(self.lines) + self.lines_below
        else:
            return max([(c.y() - self.y() + c.height()) for c in self.children]) + self.lines_below


    def width(self):
        '''return the actual width of the frame'''
        if self.width_mode == 'fixed':
            return self.max_width
        if self.lines:
            return max([len(l.content) for l in self.lines])
        else:
            return             max([(c.x() - self.x() + c.width()) for c in self.children])


    def render(self):
        '''render the frame's content or its child frames' content and store it
        as a list of lines.Line instances in self.lines.'''

        if not (self.content or self.children):
            raise RenderingError, 'Either content or children must be present.'

        # calculate max_width 
        if not self.max_width:
            self.max_width = self.parent.width() - (self.x() - self.parent.x()) - self.right_indent


     # render any content
        if self.content:
            self.lines= self.content.render(width = self.max_width)
            logger.debug('Rendered lines %s ... %s' % (self.lines[0].content, self.lines[-1].content))
            
            
        # render any children
        else:
            for c in self.children:
                c.render()



class RootFrame:
    '''Ancestor of all frames. Its render method generates the final output from the
    rendered children. The RootFrame has just children and no content.
    Future versions may add pagination, footnotes etc.'''
    
    def __init__(self, max_width = 60, paginator = None):


        self.max_width = max_width
        self.paginator = paginator
        self.children = []
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
        while len(self.cache) - 1 < y: self.cache.append(u'')
        if len(self.cache[y]) > x:
            raise LineStorageError('Line in cache is too long. (content = %s; length = %d)', self.cache[y], len(self.cache[y]))
        self.cache[y] = self.cache[y].ljust(x)
        self.cache[y] += content


    def assemble(self, frame):
        for c in frame.children: self.assemble(c)
        x = frame.x()
        y = frame.y()
        count = 0
        for l in frame.lines:
            self.store(l.content, x, y+count)
            count += 1


    def render(self):
        for c in self.children: c.render()
        for c in self.children: self.assemble(c)
        return '\n'.join(self.cache)



