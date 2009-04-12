

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
        
        
        