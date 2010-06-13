

from transcribo import logger
from frames import RootFrame, Frame
from content import ContentManager, GenericText
from factory import styles



class Page:

    def __init__(self, previous = None, page_spec = None,
        header_spec = None, footer_spec = None, translator_cfg = None):
        
        self.previous = previous
        self.page_spec = page_spec
        self.header_spec = header_spec
        self.footer_spec = footer_spec
        self.translator_cfg = translator_cfg
        self.closed = False
        # initialise position and first line within cache
        if previous: # insert this page after previous one
            self.first = previous.last + 1 
            self.y = previous.y + previous.net_length()
            self.index = previous.index + 1
        else: # this is the first page
            self.first = 0
            self.y = 0
            self.index = 0
        
        
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
                wrapper = styles['wrapper']['default'],
                **self.footer_spec['pagenumcontent_cfg'])
            GenericText(self.footer[0][0] , text = pagenum_str, translator = self.translator_cfg)
            self.footer.render()
        else:
            self.footer = None
            
        # Header: currently no headers supported
        self.header = None
        self.closed = True

            
    def render(self, cache):
    
        phys_lines = [] # list of strings each of which represents a physical line

        # top margin
        phys_lines.extend([''] * self.page_spec['top_margin'])

        # physical left margin of this page. Reconsider inner and outer margin!
        phys_margin = self.page_spec['left_margin']
        if not (self.index % 2): phys_margin += self.page_spec['inner_margin']

        if self.header:
            pass # not yet supported
            
        
        # Reference point for y position of new lines
        
        if self.previous: cur_y = self.previous.y + self.previous.net_length() - 1
        else: cur_y = -1
        
        # iterate over the lines on this page
        for l in cache[self.first : self.last + 1]:
            # insert blank lines, if necessary 
            ly = l.get_y()

            # generate new physical line or lines if necessary to reach the y position of the new line
            phys_lines.extend([''] * (ly - cur_y - 1))
            
            # add line with left margin, if new Line object has a different y pos
            # than the previous one
            if ly > cur_y:
                phys_lines.append(' ' * phys_margin)
                
            phys_lines[-1] = ''.join((phys_lines[-1].ljust(l.get_x() + phys_margin), l.render()))
            
            cur_y = ly


        # add blank lines at the bottom, if necessary to fill the page
        n = len(phys_lines) - self.page_spec['top_margin']
        if self.header: n -= 1
        phys_lines.extend([''] * (self.net_length() - n))

        # add footer
        if self.footer:
            phys_lines.append(' ' * (phys_margin + self.footer.cache[0].get_x()))
            phys_lines[-1] += self.footer.cache[0].render()

        # Add empty lines for bottom margin.
        # The extra line is necessary as otherwise the final line break would not be added by the following join.
        phys_lines.extend([''] * (self.page_spec['bottom_margin'] + 1))
        
        return self.page_spec['line_break'].join(phys_lines)
        


class Paginator:

    def __init__(self, page_spec = None, header_spec = None, footer_spec = None, translator_cfg = None):
        self.page_spec = page_spec
        self.header_spec = header_spec
        self.footer_spec = footer_spec
        self.translator_cfg = translator_cfg
        self.refs = [] # yet to be implemented
        self.targets = []
        self.width = self.get_width()


    def get_width(self):
        return (self.page_spec['width'] - self.page_spec['left_margin']
            - self.page_spec['inner_margin'] - self.page_spec['right_margin'])



    def create_pages(self, cache):
        '''
        Construct pages from the lines cache.
        Essentially, each Page instance contains pointers to the first and last
        Line object which will appear on that Page.'''
        
        # create initial empty page
        self.pages = [Page(previous = None, page_spec = self.page_spec,
            header_spec = self.header_spec, footer_spec = self.footer_spec, translator_cfg = self.translator_cfg)]
        
        pages = self.pages
        cur_page = pages[0]
        net_len = cur_page.net_length()
        
        for l in range(len(cache)):
            # put the line on current page unless the page is full or a hard
            # page break needed
            # For the semantics of page_break see in the lines module.
            
            page_break = cache[l].page_break
            
            if ((page_break == 0 and cache[l].get_y() >= cur_page.y + net_len) or # soft page break, i.e. page is full
                (page_break == 2 and cache[l].get_y() + 1 >= cur_page.y + net_len) or
                            # avoid widows and orphans, i.e.
                            # break at second last line of the page
                    (page_break == 1)): # hard page break

                # finish current page
                # set end marker of this page to the index of the previous Line object
                cur_page.last = l - 1
                cur_page.close()
                
                # create new page
                cur_page = Page(previous = cur_page, page_spec = self.page_spec,
                    header_spec = self.header_spec,
                    footer_spec = self.footer_spec, translator_cfg = self.translator_cfg)
                pages.append(cur_page)
                net_len = cur_page.net_length()
                
            else:
                # handle any references and targets. Not yet fully implemented. Please ignore.
                if cache[l].targets:
                    cache[l].page = pages.index(cur_page)
                    self.targets.append(cache[l])
                if cache[l].refs:
                    self.refs.append(cache[l])

        # close last page, if necessary
        if not cur_page.closed:
            cur_page.last = l
            cur_page.close()
        



    def render(self, cache):
        # Generate the list of pages. This will only deliver a skeleton of pages as each Page instance
        # merely contains references to its first and last Line instance in the cache.
        # The actual text of the lines will be assembled in the next step.
        self.create_pages(cache)
        
        # get string for page breaks and assemble the string of the entire
        #  document from the pages; the page.render method accesses
        # the line cache
        page_break = self.page_spec['page_break']
        result = page_break.join(p.render(cache) for p in self.pages)
        result += page_break
        return result
