

__all__ = ['frames', 'content', 'pages', 'translators']



import os.path

styles = {}

def main():
    # load styles
    from transcribo import config, preferences 
    # generate list of style files to be merged, starting with files in the package dir.
    style_files = ['/'.join((__path__[0], 'styles', fn)) for fn in preferences['styles']]
    
    # append '.yaml', if necessary
    for i in range(len(style_files)):
        if not style_files[i].endswith('.yaml'): style_files[i] += '.yaml'

    # add styles from the current dir, if any.
    if os.path.exists('styles.yaml'): style_files.append('styles.yaml')

    # load and merge the styles
    styles.update(config.Config(style_files))


