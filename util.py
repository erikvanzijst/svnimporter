import traceback
from cgi import escape
from mercurial import ui

__author__ = 'erik'

def traceback_to_str(tb):
    frames = traceback.format_list(traceback.extract_tb(tb))
    return ''.join(frames)

class MercurialUI(ui.ui):
    def __init__(self, src=None):
        ui.ui.__init__(self, src)
        if src and src.__dict__.has_key('logInfo') and src.__dict__.has_key('logError'):
            self.logInfo = src.logInfo
            self.logError = src.logError

    def write(self, *args, **opts):
        if self._buffers:
            self._buffers[-1].extend([str(a) for a in args])
        else:
            for msg in args:
                self.logInfo(escape(str(msg)))

    def write_err(self, *args, **opts):
        if self._buffers:
            self._buffers[-1].extend([str(a) for a in args])
        else:
            for msg in args:
                self.logError(escape(str(msg)))

    def flush(self):
        pass
