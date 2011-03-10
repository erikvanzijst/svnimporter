import sys
import util
import traceback

from cgi import escape
from PyQt4 import QtGui, QtCore
from mercurial import hg, ui
import hgsubversion

__author__ = 'erik'


class WizardPage(QtGui.QWizardPage):

    class _UI(ui.ui):
        # TODO: replace with util.MercurialUI
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


    class Job(QtCore.QThread):

        def __init__(self, ui, **opts):
            QtCore.QThread.__init__(self)
            self.ui = ui
            self.config = opts

        def run(self):
            try:
                self.ui.write(u'Importing <b>%s</b> into <b>%s</b>...' % (self.config['url'], self.config['dest']))
#                src = hg.repository(self.ui, self.config['url'])
#                d = hg.repository(self.ui, self.config['dest'], create=True)
#                svn_repo = hg.repository(self.ui, self.config['url'])
#                d.pull(svn_repo, heads=[])
                hg.clone(self.ui, self.config['url'], self.config['dest'])
                self.ui.write(u'Done')

            except Exception:
                type_, message, tb = sys.exc_info()
                try:
                    self.ui.write_err(escape(u'%s: %s' % (str(type_), str(message))))
                    for frame in traceback.format_list(traceback.extract_tb(tb)):
                        self.ui.write_err(escape(frame))
                except:
                    pass
                finally:
                    print util.traceback_to_str(tb)


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
        self.u.logInfo = self._info
        self.u.logError = self._error
        self.u.setconfig('ui', 'interactive', 'off')
        self.u.setconfig("ui", "formatted", None)

    def initializePage(self):
        url         = str(QtGui.QWizardPage.field(self, 'url').toString())
        username    = str(QtGui.QWizardPage.field(self, 'username').toString())
        password    = str(QtGui.QWizardPage.field(self, 'password').toString())
        dest        = str(QtGui.QWizardPage.field(self, 'localDir').toString())

        try:
            job = WizardPage.Job(self.u, **{
#                'url': url,
                'url': 'file:///home/erik/svn-repo',
                'username': username,
                'password': password,
#                'dest': dest,
                'dest': sys.argv[1]
            })
            self.connect(self, QtCore.SIGNAL('log(PyQt_PyObject)'), self.logView.appendHtml)
            job.start()

            # If we don't keep a reference to the job around, the garbage
            # collector seems to reclaim it while the background is still
            # running. This in turn makes Qt crash!
            self.job = job

        except:
            type_, message, tb = sys.exc_info()
            try:
                self._error(escape(u'%s: %s' % (str(type_), str(message))))
                for frame in traceback.format_list(traceback.extract_tb(tb)):
                    self._error(escape(frame))
            except:
                pass
            finally:
                print util.traceback_to_str(tb)

    def _info(self, msg):
        msg = str(msg)
        self.emit(QtCore.SIGNAL('log(PyQt_PyObject)'),
                  str('<div>%s</div>' % (msg[0:-1] if msg.endswith('\n') else msg)))

    def _error(self, msg):
        msg = str(msg)
        self.emit(QtCore.SIGNAL('log(PyQt_PyObject)'),
                  str(u'<div style="color: red">%s</div>' %
                      (msg[0:-1] if msg.endswith('\n') else msg)))

    def _job_finished(self):
        # TODO: disconnect signals
        pass
