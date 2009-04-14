from transcribo.renderer import RootFrame, Frame
from transcribo.renderer.content import ContentManager, BaseContent
from transcribo.renderer.page import Paginator
import unittest


class TestRenderer(unittest.TestCase):

    def setUp(self):
        self.root = RootFrame()
        self.longtext = """This text is so long that it will \
        span over multiple lines. This is useful to demonstrate the renderer's \
        behavior when dealing with lists, enumerations and such like. Also, it may be useful to demonstrate \
        the effects of hyphenation and text wrapping."""
        self.list_items = ['-', '--']
        self.enum1 = ['1.', '2.', '3.']
        self.enum2 = ['(i)', '(ii)', '(iii)']
        self.output = ''
        self.bc = BaseContent(self.longtext)
        self.cm = ContentManager(elements = [bc])
        self.frame_cfg = dict(
            x_anchor = self.root, x_hook = 'left', x_align = 'left',
            left_indent = 0, right_indent = 0,
            y_anchor = self.root, y_hook = 'bottom', y_align = 'top',
            lines_above = 1, lines_below = 0,
            max_width = 0, width_mode = 'fixed',
            max_height = 0, height_mode = 'auto')


        
    def testSimpleParagraphs(self):
        bc = BaseContent(self.longtext)
        cm = ContentManager(elements = [bc])
        f1 = Frame(parent = self.root, content = cm,
            **self.frame_cfg)
        f2_cfg = self.frame_cfg.copy()
        f2_cfg.update(lines_above = 4,
        left_indent = 2, right_indent = 3,
        y_anchor = f1, y_hook = 'bottom', y_align = 'top')
        f2 = Frame(parent = self.root, content = cm,
        **f2_cfg)
        self.output = '\n\n==========\n\n'.join((self.output, self.root.render()))
        self.assertEqual(True, True)
        


    def testTwoColumns(self):
        bc = BaseContent(self.longtext)
        cm = ContentManager(elements = [bc])
        f1_cfg = self.frame_cfg.copy()
        f1_cfg.update(max_width = 20)
        f1 = Frame(parent = self.root, content = cm,
            **f1_cfg)
        f2_cfg = self.frame_cfg.copy()
        f2_cfg.update(lines_above = 4,
        left_indent = 2, right_indent = 3,
        x_anchor = f1, x_hook = 'right', x_align = 'left',
        y_anchor = f1, y_align = 'top', y_hook = 'top',
        max_width = 30)
        f2 = Frame(parent = self.root, content = cm,
        **f2_cfg)
        self.output = '\n\n==========\n\n'.join((self.output, self.root.render()))
        self.assertEqual(True, True)



    def testLists(self):
        f1_cfg = self.frame_cfg.copy()
        f1_cfg.update(max_width = 20)
        list_body = Frame(parent = self.root, content = self.cm,
            **f1_cfg)
        f2_cfg = self.frame_cfg.copy()
        f2_cfg.update(lines_above = 4,
        left_indent = 2, right_indent = 3,
        x_anchor = f1, x_hook = 'right', x_align = 'left',
        y_anchor = f1, y_align = 'top', y_hook = 'top',
        max_width = 30)
        f2 = Frame(parent = self.root, content = cm,
        **f2_cfg)
        self.output = '\n\n==========\n\n'.join((self.output, self.root.render()))
        self.assertEqual(True, True)




    def tearDown(self):
        output_file = open('test1.outt', 'a')
        output_file.write(self.output)
        output_file.close()
        

# if __name__ == '__main__':
#     unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(TestRenderer)
unittest.TextTestRunner(verbosity=2).run(suite)

