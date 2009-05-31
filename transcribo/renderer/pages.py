

from transcribo import logger
from frames import BuildingBlock, RootFrame, Frame
from content import ContentManager, GenericText
import styles



class Page(BuildingBlock):

    def __init__(self, parent, page_spec = None,
        header_spec = None, footer_spec = None, translator_cfg = None):

        self.parent = parent
        self.page_spec = page_spec
        self.header_spec = header_spec
        self.footer_spec = footer_spec
        self.translator_cfg = translator_cfg
        
    def setup(self):
        # index of this page in the page list
        parent = self.parent
        self.index = index = parent.pages.index(self)
        # Index and y-coord of first line on this page in the line cache
        if index == 0:
            self.first = 0
            self.y = 0
        else:
            previous_page = parent.pages[index - 1]
            self.first = previous_page.last + 1 # caller must make sure that this line exists in cache.
            self.y = previous_page.y + previous_page.net_length()
        self.last = self.first # index of last line on this page in line cache


    def get_width(self):
        return (self.page_spec['width'] - self.page_spec['left_margin']
            - self.page_spec['inner_margin'] - self.page_spec['right_margin'])

    def gross_length(self):
        return self.page_spec['length'] - self.page_spec['top_margin'] - self.page_spec['bottom_margin']

    def net_length(self):
        result = self.gross_length()
        if self.header_spec: result -= 1
        if self.footer_spec: result -= 1
        return result

    def close(self):
        '''Create header and footer.
        This is all hard-coded and needs to be made more configurable.'''
        
        if self.footer_spec:
            self.footer = RootFrame(max_width = self.get_width())
            # frame for page number on the right. Alternation to be added.
            Frame(self.footer,
                x_anchor = self.footer, y_anchor = self.footer,
                **self.footer_spec['pagenum_cfg'])
            # Generate page number string
            pagenum_str = str(self.index + 1)
            ContentManager(self.footer[0],
                wrapper = styles.wrappers['simple'],
                **self.footer_spec['pagenumcontent_cfg'])
            GenericText(self.footer[0][0] , text = pagenum_str, translator = self.translator_cfg)
            self.footer.render()
        else:
            self.footer = None
        # Header: currently no headers supported
        self.header = None

            
    def render(self, cache):
        logger.info('Rendering page. first = %d, last = %d.' % (self.first, self.last))
        phys_lines = []
        
        # physical left margin of this page
        n = self.page_spec['left_margin']
        if not (self.index % 2): n += self.page_spec['inner_margin']
        phys_margin = ' ' * n

        if self.header:
            pass # not yet supported
            
        # the following serves to distinguish logical lines that will occur
        # on the same physical line as the previous one from new physical lines
        # Example: bullet lists.
        prev_y = -1
        
        # iterate over the lines on this page
        for l in cache[self.first : self.last + 1]:
            # insert blank lines, if necessary
            ly = l.y()
            i = self.y
            while i < ly:
                phys_lines.append('')
                i += 1

            # generate new non-empty physical line, if necessary
            if prev_y < ly:
                phys_lines.append(phys_margin)
            
            # line-specific  indentation
            phys_lines[-1] = phys_lines[-1].ljust(l.x() + len(phys_margin))
            
            # add the actual line content
            phys_lines[-1] += str(l)
            prev_y = ly
            
        # add blank lines at the bottom, if necessary
        while len(phys_lines) < self.net_length():
            phys_lines.append('')

        # add footer
        if self.footer:
            phys_lines.append(phys_margin)
            for l in self.footer.cache:
                phys_lines[-1] = phys_lines[-1].ljust(len(phys_margin) + l.x())
                phys_lines[-1] += str(l)
                
        return '\n'.join(phys_lines)

            
            

class Paginator:

    def __init__(self, page_spec = None, header_spec = None, footer_spec = None, translator_cfg = None):
        self.page_spec = page_spec
        self.header_spec = header_spec
        self.footer_spec = footer_spec
        self.translator_cfg = translator_cfg
        self.refs = []
        self.targets = []
        self.pages = []
        self.pages.append(Page(self, page_spec = self.page_spec,
            header_spec = self.header_spec, footer_spec = self.footer_spec, translator_cfg = self.translator_cfg))
        self.pages[0].setup()
        self.width = self.pages[0].get_width()


    def create_pages(self, cache):
        pages = self.pages
        cur_page = pages[-1]
        logger.info('creating pages for cache of length %d. ' % len(cache))
        for l in cache:
            # does this line fit on current page?
            if cur_page.y <= l.y() <= cur_page.y + cur_page.net_length():
                cur_page.last = cache.index(l)
                if l.targets:
                    l.page = pages.index(cur_page)
                    self.targets.append(l)
                if l.refs:
                    self.refs.append(l)
            else:
                # create new page
                cur_page.close()
                logger.info('New page at cache index %d' % cache.index(l))
                pages.append(Page(self, page_spec = self.page_spec,
                    header_spec = self.header_spec,
                    footer_spec = self.footer_spec, translator_cfg = self.translator_cfg))
                cur_page = pages[-1]
                cur_page.setup()
                logger.info('Page successfully created.')

        # close last page
        cur_page.close()
        logger.info('Last page closed')
        
        # resolve page references (to be implemented)



    def render(self, cache):
        logger.info('Positions of lines: %s' % str([(l.x(), l.y(), str(l)) for l in cache]))
        self.create_pages(cache)
        page_break = self.page_spec['page_break']
        result = page_break.join((p.render(cache) for p in self.pages))
        result += page_break
        return result
