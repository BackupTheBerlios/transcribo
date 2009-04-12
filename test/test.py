from transcribo.renderer import RootFrame, Frame
from transcribo.renderer.content import ContentManager, BaseContent
import unittest


class TestRenderer(unittest.TestCase):

    def setUp(self):
        self.root = RootFrame()
        self.text1 = open('test_text1.txt', 'r').read()

        
    def testSingleFrame(self):
        bc = BaseContent(self.text1)
        cm = ContentManager(elements = [bc])
        Frame(parent = self.root, content = cm, width_from = self.root, height_from = self.root,
        x_from = self.root, y_from = self.root,
            max_width = 0)
        output = self.root.render()
        open('test_text1.out', 'w').write(output)
        self.assertEqual(4, 2+2)
        


# if __name__ == '__main__':
#     unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(TestRenderer)
unittest.TextTestRunner(verbosity=2).run(suite)

