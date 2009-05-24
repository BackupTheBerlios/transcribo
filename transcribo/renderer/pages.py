

from frames import BuildingBlock, RootFrame, Frame
import styles



'''number conversion for enumerated_list'''


from roman import toRoman


def to_arabic(n):
    return str(n)


def to_loweralpha(n):
    digits = []
    while n:
        digits.append(chr((n % 26) + 96))
        n = n // 26
    digits.reverse()
    return ''.join(digits)


def to_upperalpha(n):
    return to_loweralpha(n).upper()

def to_lowerroman(n):
    return toRoman(n).lower()

def to_upperroman(n):
    return toRoman(n)

class Page(BuildingBlock):

    def __init__(self, parent, pagenum, **page_spec):
        index = parent.index(self)
        if index == 0: self.first = 0
        else:
            self.first = parent[index-1].last + 1
        self.parent = parent
        for k,v in page_spec:
            setattr(self, k, v)
        self.page_num_str = self.get_pagenum_str()
        self.header = self.get_deco(**self.header)
        self.footer = self.get_deco(**self.footer)
        self.lines = self.net_lines()
        self.max_y = self.parent[start].y() + self.lines
        

    def get_width(self):
        return self.width - self.left_margin - self.inner_margin - self.right_margin

    def gross_length(self):
        return self.length - self.top_margin - self.bottom_margin

    def net_length(self):
        result = self.gross_length()
        if self.header: result -= 1
        if self.footer: result -= 1
        return result




class PageNumber:

    def __init__(self,
        start = 1, format = 'arabic', prefix = '', suffix = '',
        position = 'up-right', first_page = False):

        
                self.start = start
        self.prefix = prefix
        self.suffix = suffix
        self.count = start
        self.position = position

    def as_string(page_number):
        return ''.join((self.prefix,
            __dict__['to' + self.format](page_number),
            self.suffix))




class Paginator:

    def __init__(self, page_spec, pagenum_spec, header_spec, footer_spec):
        self.page_spec = page_spec
        self.pagenum_spec = pagenum_spec
        self.header_spec = header_spec
        self.footer_spec = footer_spec
        self.cache = []
        self.pages = []


    def create_pages(self):
        pages = self.pages
        cache = self.cache
        cache_index = 0
        while cache_index < len(cache):
            # create new page 
            pages.append(Page(self.page_spec, self.pagenum_spec, self.header_spec, self.footer_spec))
            # fill new page with lines
            while cache[cache_index].y() <= cur_page.last: cache_index += 1
            i = first
            while cache and pages[-1].hasspace(cache[i].y()):
                # if line contains an unresolved reference, render it.
                if hasattr(cache[i], 'render'):
                    is_rendered = cache[i].render(page_number = pages[-1].page_number)
                    if not is_rendered: # e.g. because reference replacement makes line too long
                        cache[i].frame.render()
                            

                
                cur_page.add(self.cache.pop(0))
            cur_page.close()
                
