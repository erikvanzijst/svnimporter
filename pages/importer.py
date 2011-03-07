import sys
from hgsubversion.svnrepo import svnremoterepo
import util
import traceback

from cgi import escape
from PyQt4 import QtGui, QtCore
from mercurial import hg, ui
from hgsubversion import svnrepo

__author__ = 'erik'


class WizardPage(QtGui.QWizardPage):

    class _UI(ui.ui):
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

        # Signals:
        info = QtCore.pyqtSignal(str, name='info')
        error = QtCore.pyqtSignal(str, name='error')
        progress = QtCore.pyqtSignal(int, name='progress')

        def __init__(self, ui, **opts):
            QtCore.QThread.__init__(self)
            self.ui = ui
            self.config = opts

        def run(self):
            try:
                self.info.emit(u'Importing <b>%s</b> into <b>%s</b>...' % (self.config['url'], self.config['dest']))
                src = svnremoterepo(self.ui, self.config['url'])
                hg.clone(self.ui, src, self.config['dest'])
                self.info.emit(u'Done')

            except Exception:
                type_, message, tb = sys.exc_info()
                try:
                    self.error.emit(escape(u'%s: %s' % (str(type_), str(message))))
                    for frame in traceback.format_list(traceback.extract_tb(tb)):
                        self.error.emit(escape(frame))
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
        dest        = str(QtGui.QWizardPage.field(self, 'output').toString())

        try:
            job = WizardPage.Job(self.u, **{
                'url': url,
                'username': username,
                'password': password,
                'dest': dest
            })
            job.info.connect(self._info)
            job.error.connect(self._error)
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
                    self._error.emit(escape(frame))
            except:
                pass
            finally:
                print util.traceback_to_str(tb)

    def _info(self, msg):
        msg = str(msg)
        self.logView.appendHtml(u'<div>%s</div>' % (msg[0:-1] if msg.endswith('\n') else msg))

    def _error(self, msg):
        msg = str(msg)
        self.logView.appendHtml(u'<div style="color: red">%s</div>' % (msg[0:-1] if msg.endswith('\n') else msg))

    def _job_finished(self):
        # TODO: disconnect signals
        pass
