"""
Transcribo Test
This script contains the following unittests:

a test of the rst reader. It processes all .rst files in the ./rst subdir
as well as the readme.txt file.

"""


from transcribo import logger
import unittest, os



class TestRenderer(unittest.TestCase):

    def setUp(self): pass

    def test_rst(self):
        '''tests for the rST front end. Processes ../README.txt and all *.rst files in the ./rst subdir.'''

        from transcribo import Transcriber

        input_files = ['../README.txt']
        input_files.extend(['./rst/' + name for name in os.listdir('./rst') if name.endswith('.rst')])
        t = Transcriber(cmd_line = False, styles = ['test'])
        for name in input_files:
            logger.info('testrST: Processing %s...' % name)
            t.transcribe_file(infile = name,
                outfile = name[:-4] + '.out')




    def tearDown(self): pass
        
def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRenderer)
    unittest.TextTestRunner(verbosity=2).run(suite)


run()
        

# if __name__ == '__main__':
#     unittest.main()
# suite = unittest.TestLoader().loadTestsFromTestCase(TestRenderer)
# unittest.TextTestRunner(verbosity=2).run(suite)




