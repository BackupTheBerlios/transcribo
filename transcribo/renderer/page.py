

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




class Paginator:


    def __init__(self, width = 60, left_margin = 2, right_margin = 2, inner_margin = 1,
        length = 60, top_margin = 3, bottom_margin = 2,
        page_num = None):
        
        self.width = width
        self.left_margin = left_margin
        self.right_margin = right_margin
        self.inner_margin = inner_margin
        self.length = length
        self.top_margin = top_margin
        self.bottom_margin = bottom_margin
        self.page_num = page_num
        
        
    def get_width(self):
        return self.width - self.left_margin - self.inner_margin - self.right_margin
        
    def gross_length(self):
        return self.length - self.top_margin - self.bottom_margin
        
    def net_length(self):
        result = self.gross_length()
        if self.header: result -= 1
        if self.footer: result -= 1
        return result
        
    def page_no(self, line_index):
        return line_index // self.net_page_length()
    


class PageNumber:



    def __init__(self, paginator = None, start = 1, format = 'arabic',
            prefix = '', suffix = '', position = 'up-right', first_page = False):

        self.paginator = paginator
        self.start = start
        self.prefix = prefix
        self.suffix = suffix
        self.count = start
        self.position = position
        self.converters = dict(arabic = to_arabic,
            loweralpha = to_loweralpha, upperalpha = to_upperalpha,
            lowerroman = to_lowerroman,
            upperroman = to_upperroman)
        
        
    def as_string(page_number):
        return ''.join((self.prefix,
            self.converters[self.format](page_number),
            self.suffix))
        

    
