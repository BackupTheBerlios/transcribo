import logging

# Set up logging to the console and the log file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    filename ='transcribo.log')

standard_handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
standard_handler.setFormatter(formatter)
logging.getLogger('').addHandler(standard_handler)
logger =logging.getLogger('transcribo')

__all__ = ['renderer', 'rst2txt']