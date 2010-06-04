

__all__ = ['frames', 'content', 'pages', 'translators']



import os.path

styles = {}

def main():
    # load styles
    from transcribo import config, preferences 
    # generate list of style files to be merged, starting with files in the package dir.
    style_files = ['/'.join((__path__[0], 'styles', fn)) for fn in preferences['styles']]

    # add styles from the current dir, if any. This is presently only 1 file.
    if os.path.exists('styles.yaml'): style_files.append('styles.yaml')

    # load and merge the styles
    styles.update(config.Config(style_files))


