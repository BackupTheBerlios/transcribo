# Transcribo Test
# This script contains one unittest rendering a nested enumeration. This
# serves to demonstrate the configuration of the Frame and content objects including the
# use of translators.
# The configuration of the YABT and Louis Braille translators is though commented out as few
# users will have the package installed. Those interested will find the URL of the YABT website in
# transcribo/render/translator.py.


from transcribo.renderer.frames import RootFrame, Frame
from transcribo import logger
from transcribo.renderer.content import ContentManager, GenericText
from transcribo.renderer import styles, pages
import unittest


class TestRenderer(unittest.TestCase):

    def setUp(self):
        self.paginator = pages.Paginator(page_spec = styles.pages['default'],
        header_spec = None, footer_spec = styles.footers['default'],
        translator_cfg = styles.translators['default'])
        self.root = RootFrame(max_width = self.paginator.width)
        self.longtext = """I have just returned from a visit to my landlord - the solitary
neighbour that I shall be troubled with. This is certainly a beautiful country!
In all England, I do not believe that I could have fixed on a situation so
completely removed from the stir of society. A perfect misanthropist's heaven:
and Mr. Heathcliff and I are such a suitable pair to divide the desolation
between us. A capital fellow! He little imagined how my heart warmed towards him
when I beheld his black eyes withdraw so suspiciously under their brows, as I
rode up, and when his fingers sheltered themselves, with a jealous resolution,
still further in his waistcoat, as I announced my name. """ * 5


        self.output = ''
            


    def testEnum(self):
    
        def create(outer, previous, symbols):
            # create frame containing the whole list
            container_cfg = dict(
                x_anchor = previous, x_align = 'left', x_hook = 'left', x_offset = 0,
                y_anchor = previous, y_align = 'top', lines_below = 0,
                max_width = 0, width_mode = 'fixed',
                max_height = 0, height_mode = 'auto')
            if previous is outer: container_cfg.update(y_hook = 'top', y_offset = 0)
            else: container_cfg.update(y_hook = 'bottom', y_offset = 0)
            container = Frame(outer, **container_cfg)
            previous = container

            # Go through the nested enumeration
            for s in symbols:
                if type(s) == list:
                    previous = create(container, previous, s)
                else:
                    # create frame for the enumerator
                    enum_cfg = dict(
                        x_anchor = container, x_align = 'left', x_hook = 'left', x_offset = 1,
                        y_anchor = previous, y_align = 'top',
                        max_width = 4, width_mode = 'fixed',
                        max_height = 1, height_mode = 'fixed')
                    if previous is not container:
                        enum_cfg.update(y_hook = 'bottom', y_offset = 0)
                    else:
                        enum_cfg.update(y_hook = 'top', y_offset = 0)
                    enum = Frame(container, **enum_cfg)
                    content = ContentManager(parent = enum, x_align = 'right', wrapper = styles.wrappers['simple'])
                    GenericText(content, text = s)
                    
                    
                    # choose a translator from the list (see below)
                    cur_translator = translator_cfg[symbols.index(s)]
                    
                    # create the paragraph
                    para_cfg = dict(
                        x_anchor = enum, x_hook = 'right', x_align = 'left', x_offset = 1,
                        y_anchor = enum, y_hook = 'top', y_align = 'top', y_offset = 0,
                        max_width = 0, width_mode = 'fixed',
                        max_height = 0, height_mode = 'auto', lines_below = 2)
                    previous = Frame(container, **para_cfg)
                    content = ContentManager(parent = previous, wrapper = styles.wrappers['simple'], translator = cur_translator)
                    GenericText(content, text = self.longtext)
            return container
                    
                
        structure = ['I.', 'II.', 'III.', ['1.', '2.'], 'IV.', ['1.', '2.', '3.', ['a)', 'b)']], 'V.']
        
        # Some translator configurations. The create method above will choose
        # amongst them. Each position in the following list corresponds
        # to a number in the enumeration, so that each translator
        # will be invoked.
        
        translator_cfg = [None, # no translator
            dict(class_path = 'translators.UpperTrans'), # uppercase translator
            # dict(class_path = 'translators.YABTrans', state = 2), # Braille grade 2
            dict(class_path = 'translators.Louis', tables = ['en-US-g2.ctb']),
            None, None, None, None, None]
            
            # create the frames
        logger.info('Creating frames')
        create(self.root, self.root, structure)
        logger.info('Rendering frames.')
        self.root.render()
        # create the pages
        logger.info('Creating pages')
        self.output = self.paginator.render(self.root.cache)
        self.assertEqual(True, True)


    def test_plaintext(self):
        from transcribo.plaintext import Writer
        w = Writer()
        self.output = w.render(self.longtext)
        



    def tearDown(self):
        output_file = open('test1.out', 'w')
        output_file.write(self.output)
        output_file.close()

def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRenderer)
    unittest.TextTestRunner(verbosity=2).run(suite)

run()
        

# if __name__ == '__main__':
#     unittest.main()
# suite = unittest.TestLoader().loadTestsFromTestCase(TestRenderer)
# unittest.TextTestRunner(verbosity=2).run(suite)




