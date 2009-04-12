# Transcribo - a library to convert various file formats into plain text

__all__ = ['core', 'contenttypes', 'lines', 'singleton']

from transcribo import logger



class FrameError(Exception):
    def __init__(self, *args, **args2):
        Exception.__init__(*args, **args2)
        logger.error('FrameError: %s', self.__str__)



class Frame:
    '''display within the parent frame.
    left_indent and right_indent: distance to the parent's border.
        Any text between the frame and the left border will be left untouched
        rather than replace it by spaces.
    lines_above: distance to the upper border of parent or the upper sibling
    # lines below: distance to the lower sibling
    height: depending on the content; no upper limit

    '''

    def __init__(self, parent, content,
        width_from, height_from, x_from, y_from,
        max_width, max_height = 0,
        width_mode = 'auto', height_mode = 'auto',
        x_align = 'left', y_align = 'bottom',
        left_indent = 0, right_indent = 0,
        lines_above = 0, lines_below = 0):

        self.content = content
        self.parent = parent
        self.children = []
        parent.children.append(self)
        self.max_width = max_width
        self.max_height = max_height
        self.width_from = width_from
        self.height_from = height_from
        self.width_mode = width_mode
        self.height_mode = height_mode
        self.x_from = x_from
        self.x_align = x_align
        self.y_from = y_from
        self.y_align = y_align
        self.left_indent = left_indent
        self.right_indent = right_indent
        self.lines_above = lines_above
        self.lines_below = lines_below
        self.lines = []
        logger.info('Created StandardFrame with max_width = %d and max_height = %d', self.max_width, self.max_height)

    def x(self):
            # horizontal position
        if self.x_align == 'left':
            return self.x_from.x() + self.left_indent
        elif self.x_align == 'right':
            return  self.x_from.x() + self.x_from.width() - self.right_indent - self.width()
        elif self.x_align == 'centered':
            return self.x_from.x() + int(self.x_from.width() / 2) - int(self.width() / 2)

    def y(self):
        # vertical position
        if self.y_align == 'top':
            return self.y_from.y() + self.y_from.lines_above
        elif self.y_align == 'bottom':
            return self.y_from.y() + self.y_from.height()
        elif self.y_align == 'centered':
            return self.y_from.y() + int(self.y_from.height() / 2) - int(self.height() / 2)

    def height(self):
        # Determine actual frame height
        if self.lines:
            result = len(self.lines) - self.lines_above - self.lines_below
        else:
            result = max([(c.y() - self.y() + c.height()) for c in self.children])
        if self.max_height != 0 and result > self.max_height:
            raise FrameError('Too many lines in content.')
        else:
            return result


    def width(self):
        if self.width_mode == 'fixed':
            return self.max_width
        else:
            if lines:
                return max([l.length() for l in self.lines])
            else:
                return             max([(c.x() - self.x() + c.width()) for c in self.children])


    def render(self):

        if not (self.content or self.children):
            raise FrameError('Either content or children must be present.')

        # calculate max_width and max_hight
        if not self.max_width:
            self.max_width = self.width_from.width() - self.left_indent - self.right_indent
            self.width_mode = 'fixed'
        if not self.max_height and self.height_from:
            self.max_height = self.height_from.height()
            self.hight_mode = 'fixed'


        # Add lines above
        for i in range(self.lines_above):
            self.lines.append(Line(''))

        # render any content
        if self.content:
            self.lines = self.content.render()

        # render any children
        else:
            for c in self.children:
                c.render()

        # add empty lines below
        for i in range(self.lines_below):
            self.lines.append(Line(''))

# check for excess of max_height?



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
            raise FrameError('Line in cache is too long.')
        self.cache[y] = self.cache[y].ljust(x)
        self.cache[y] += content


    def assemble(self, frame):
        for c in frame.children: assemble(c)
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



