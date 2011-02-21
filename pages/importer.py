import sys
import traceback
from PyQt4 import QtGui
from mercurial import hg, ui

__author__ = 'erik'


class WizardPage(QtGui.QWizardPage):

    class _UI(ui.ui):
        def __init__(self, src=None):
            ui.ui.__init__(self, src)
            if src and src.__dict__.has_key('logView'):
                self.logView = src.logView

        def write(self, *args, **opts):
            if self._buffers:
                self._buffers[-1].extend([str(a) for a in args])
            else:
                print type(self.logView)
                for msg in args:
                    msg = str(msg)
                    self.logView.appendHtml(u'<div>%s</div>' % (msg[0:-1] if msg.endswith('\n') else msg))

        def write_err(self, *args, **opts):
            if self._buffers:
                self._buffers[-1].extend([str(a) for a in args])
            else:
                print type(self.logView)
                for msg in args:
                    msg = str(msg)
                    self.logView.appendHtml(u'<div style="color: red">%s</div>' % (msg[0:-1] if msg.endswith('\n') else msg))

        def flush(self):
            pass


    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)

        grid = QtGui.QGridLayout()

        description = QtGui.QLabel(u'Converting...')
        grid.addWidget(description, 0, 0)

        self.logView = QtGui.QPlainTextEdit()
        self.logView.setReadOnly(True)
        grid.addWidget(self.logView, 1, 0)

        self.setLayout(grid)

        self.u = WizardPage._UI()
        self.u.logView = self.logView
        self.u.setconfig('ui', 'interactive', 'off')
        self.u.setconfig("ui", "formatted", None)

    def _write_tb(self, tb):
        stack = traceback.format_list(traceback.extract_tb(tb))
        for line in stack:
            self.u.write_err(line)

    def initializePage(self):
        url         = str(QtGui.QWizardPage.field(self, 'url').toString())
        username    = str(QtGui.QWizardPage.field(self, 'username').toString())
        password    = str(QtGui.QWizardPage.field(self, 'password').toString())
        dest        = str(QtGui.QWizardPage.field(self, 'output').toString())


        self.u.write(u'Importing %s into %s...' % (url, dest))
        try:
            src = hg.repository(self.u, url)
            hg.clone(self.u, src, dest)
            self.u.write(u'Done')

        except Exception:
            self.u.write_err(u'%s: %s' % (str(sys.exc_info()[0]), str(sys.exc_info()[1])))
            self._write_tb(sys.exc_info()[2])
