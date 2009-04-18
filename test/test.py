from transcribo.renderer import RootFrame, Frame, logger
from transcribo.renderer.content import ContentManager, BaseContent
from transcribo.renderer.page import Paginator
import unittest


class TestRenderer(unittest.TestCase):

    def setUp(self):
        self.root = RootFrame(max_width = 80)
        self.longtext = """This text is so long that it will\
                        span over multiple lines. This is useful to demonstrate the renderer's\
                        behavior when dealing with lists, enumerations and such like. Also, it may be useful to demonstrate\
                        the effects of hyphenation and text wrapping."""
        self.output = ''
        self.bc = BaseContent(self.longtext)
        self.cm = ContentManager(elements = [self.bc])
        self.frame_cfg = dict(
            x_anchor = self.root, x_hook = 'left', x_align = 'left',
            left_indent = 0, right_indent = 0,
            y_anchor = self.root, y_hook = 'bottom', y_align = 'top',
            lines_above = 1, lines_below = 0,
            max_width = 0, width_mode = 'fixed',
            max_height = 0, height_mode = 'auto')



    def testEnum(self):
    
        def create(outer, previous, symbols):
            # create frame containing the whole list
            container_cfg = dict(parent = outer, content = None,
                x_anchor = previous, x_align = 'left', x_hook = 'left', left_indent = 0,
                y_anchor = previous, y_align = 'top', lines_below = 0,
                max_width = 0, width_mode = 'fixed',
                max_height = 0, height_mode = 'auto')
            if previous is outer: container_cfg.update(y_hook = 'top', lines_above = 0)
            else: container_cfg.update(y_hook = 'bottom', lines_above = 0)
            container = Frame(**container_cfg)
            previous = container

            # Go through the nested enumeration
            for s in symbols:
                if type(s) == list:
                    previous = create(container, previous, s)
                else:
                    # create frame for the enumerator
                    enum_cfg = dict(parent = container,
                        content = ContentManager(elements = [BaseContent(content = s)], align = 'right'),
                        x_anchor = container, x_align = 'left', x_hook = 'left', left_indent = 1,
                        y_anchor = previous, y_align = 'top',
                        max_width = 4, width_mode = 'fixed',
                        max_height = 1, height_mode = 'fixed')
                    if previous is not container:
                        enum_cfg.update(y_hook = 'bottom', lines_above = 0)
                    else:
                        enum_cfg.update(y_hook = 'top', lines_above = 0)
                    enum = Frame(**enum_cfg)
                    # create the paragraph
                    para_cfg = dict(
                        parent = container,
                        content = ContentManager(elements = [BaseContent(content = self.longtext)]),
                        x_anchor = enum, x_hook = 'right', x_align = 'left', left_indent = 1,
                        y_anchor = enum, y_hook = 'top', y_align = 'top', lines_above = 0,
                        max_width = 0, width_mode = 'fixed',
                        max_height = 0, height_mode = 'auto')
                    previous= Frame(**para_cfg)
            return container
                    
                
        structure = ['I.', 'II.', 'III.', ['1.', '2.'], 'IV.', ['1.', '2.', '3.', ['a)', 'b)']], 'V.']
        create(self.root, self.root, structure)
        self.output = '\n\n==========\n\n'.join((self.output, self.root.render()))
        self.assertEqual(True, True)




    def tearDown(self):
        output_file = open('test1.out', 'a')
        output_file.write(self.output)
        output_file.close()
        

# if __name__ == '__main__':
#     unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(TestRenderer)
unittest.TextTestRunner(verbosity=2).run(suite)

