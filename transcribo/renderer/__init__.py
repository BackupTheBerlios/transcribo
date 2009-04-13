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

    def __init__(self, parent, content,
        x_anchor, x_hook, x_align,
        left_indent, right_indent,
        y_anchor, y_hook,y_align,
        lines_above, lines_below,
        width_from, max_width, width_mode,
        height_from, max_height, height_mode):

        self.parent = parent
        self.content = content
        self.children = []
        parent.children.append(self)
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
        self.lines_below = lines_below
        # width
        self.width_from = width_from # same width as another frame
        self.max_width =  max_width
        self.width_mode = width_mode # 'fixed' or 'auto', i.e. the content determines the width
        # height
        self.height_from = height_from
        self.max_height =  max_height
        self.height_mode = height_mode):
        
        
    def x(self):
        # horizontal position
        result = self.x_anchor.x()
        if self.x_align == 'left':
            result = result + self.left_indent # x_anchor.right_indent is ignored here. Meaningful? Use max. of both instead?
        elif: self.x_align == 'right':
            result = result - self.width() - self.right_indent
        elif: self.x_align == 'center':
            result = result - self.width() // 2 # left- and right_indent are ignored here. Meaningful?
        if self.x_hook == 'left': pass # this could be omitted, but it's more clear.
        elif: self.x_hook == 'right':
            result = result + self.width_from.width()
        elif: x_hook == 'center':
            result += self.width_from.width() // 2
        return result

            

    def y(self):
        # vertical position
        result = self.y_anchor.y()
        if self.y_align == 'top':
            result = result + self.lines_above
        elif: self.y_align == 'bottom':
            result = result - self.height() - self.lines_below
        elif: self.y_align == 'center':
            result = result - self.height() // 2 # left- and right_indent are ignored here. Meaningful?
        if self.y_hook == 'top': # this could be omitted, but it's more clear.
            pass
        elif: self.y_hook == 'bottom':
            result = result + self.height_from.height()
        elif: y_hook == 'center':
            result += self.height_from.height() // 2
        return result

        
    def height(self):
        # Determine actual frame height
        if self.height_mode == 'fixed':
            return self.max_height
        if self.lines:
            return len(self.lines)
        else:
            return max([(c.y() - self.y() + c.height()) for c in self.children])


    def width(self):
        if self.width_mode == 'fixed':
            return self.max_width
        if lines:
            return max([l.length() for l in self.lines])
        else:
            return             max([(c.x() - self.x() + c.width()) for c in self.children])


    def render(self):

        if not (self.content or self.children):
            raise RenderingError, 'Either content or children must be present.'

        # calculate max_width and max_hight
        if not self.max_width:
            self.max_width = self.width_from.width() - self.left_indent - self.right_indent
        if not self.max_height:
            self.max_height = self.height_from.height() # lines_above and lines_below are ignored here. Meaningful?


        # Add lines above
        for i in range(self.lines_above):
            self.lines.append(Line(content = ''))

        # render any content
        if self.content:
            self.lines.extend(self.content.render(width = self.max_width))
            # prepend indentation
            indent_str = ' ' * self.left_indent
            for l in self.lines: l = indent_str + l
            logger.debug('Rendered lines %s ... %s' % (self.lines[0], self.lines[-1]))
            
            
        # render any children
        else:
            for c in self.children:
                c.render()

        # add empty lines below
        for i in range(self.lines_below):
            self.lines.append(Line(''))

    # check for excess of max_height
    if self.max_heiht and len(self.lines) > self.max_height:
        raise RenderingError('Too many lines in frame (%d allowed, %d given).' % (self.max_height, len(self.lines)))

    




class RootFrame:

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
        # logger.debug('Storing line at x = %d, y = %d.', x,y)
        while len(self.cache) - 1 < y: self.cache.append(u'')
        if len(self.cache[y]) > x:
            raise LineStorageError, 'Line in cache is too long.'
        self.cache[y] = self.cache[y].ljust(x)
        self.cache[y] += content


    def assemble(self, frame):
        for c in frame.children: assemble(c)
        x = frame.x()
        y = frame.y()
        count = 0
        for l in frame.lines:
            logger.debug('Storing line with content (%s) at position (x,y) = (%d, %d).' % (l.content, x, y+count))
            self.store(l.content, x, y+count)
            count += 1


    def render(self):
        for c in self.children: c.render()
        for c in self.children: self.assemble(c)
        return '\n'.join(self.cache)



