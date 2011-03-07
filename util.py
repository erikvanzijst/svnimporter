import traceback

__author__ = 'erik'

def traceback_to_str(tb):
    frames = traceback.format_list(traceback.extract_tb(tb))
    return ''.join(frames)