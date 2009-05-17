

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
        # page numbering:
        start = 1, format = 'arabic', prefix = '', suffix = '',
        position = 'up-right', first_page = False):


        self.width = width
        self.left_margin = left_margin
        self.right_margin = right_margin
        self.inner_margin = inner_margin
        self.length = length
        self.top_margin = top_margin
        self.bottom_margin = bottom_margin
        self.start = start
        self.prefix = prefix
        self.suffix = suffix
        self.count = start
        self.position = position

        
        
    def get_width(self):
        return self.width - self.left_margin - self.inner_margin - self.right_margin
        
    def gross_length(self):
        return self.length - self.top_margin - self.bottom_margin
        
    def net_length(self):
        result = self.gross_length()
        if self.header: result -= 1
        if self.footer: result -= 1
        return result
        
    def line2page(self, line_index):
        return line_index // self.net_page_length()

        
    def as_string(page_number):
        return ''.join((self.prefix,
            __dict__['to' + self.format](page_number),
            self.suffix))
        

class PageBreak:

    def __init__(self, string = '\n\n\n'):
        self.string = string
        
    def __str__(self):
        return self.string
        
        
