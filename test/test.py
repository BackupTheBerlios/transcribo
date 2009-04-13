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
        self.frame_cfg = dict(
            x_from = None, x_rel = 'left', x_align = 'left',
            left_indent = 0, right_indent = 0,
            y_from = None, y_rel = 'bottom',y_align = 'top',
            lines_above = 0, lines_below = 1,
            width_from = None, max_width = 0, width_mode = 'fixed',
            height_from = None, max_height = 0, height_mode = 'auto')


        
    def testSimpleParagraphs(self):
        bc = BaseContent(self.longtext)
        cm = ContentManager(elements = [bc])
        f1 = Frame(parent = self.root, content = cm,
            **self.frame_cfg.update(x_from = self.root, width_from = self.root,
            *   y_from = self.root, height_from = self.root))
        f2 = Frame(parent = self.root, content = cm,
        **self.frame_cfg.update(width_from = f1, height_from = self.root,
        x_from = f1, y_from = f1,
        lines_above = 4,
        left_indent = 2, right_indent = 3)
        self.output = '\n\n==========\n\n'.join(self.output, self.root.render())
        self.assertEqual(True, True)
        


    def testTwoColumns(self):
        bc = BaseContent(self.longtext)
        cm = ContentManager(elements = [bc])
        f1 = Frame(parent = self.root, content = cm,
            **self.frame_cfg.update(x_from = self.root, width_from = self.root,
            *   y_from = self.root, height_from = self.root))
        f2 = Frame(parent = self.root, content = cm,
        **self.frame_cfg.update(width_from = f1, height_from = self.root,
        x_from = f1, y_from = f1,
        lines_above = 4,
        left_indent = 2, right_indent = 3)
        lines_above = 4,
        self.output = '\n\n==========\n\n'.join(self.output, self.root.render())
        self.assertEqual(True, True)

    def tearDown(self):
        output_file = open('test1.outt', 'w')
        output_file.write(self.output)
        output_file.close()
        

# if __name__ == '__main__':
#     unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(TestRenderer)
unittest.TextTestRunner(verbosity=2).run(suite)

