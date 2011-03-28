import subprocess
import sys
import util
import traceback

from cgi import escape
from PyQt4 import QtGui, QtCore

__author__ = 'erik'

class WizardPage(QtGui.QWizardPage):

    class Job(QtCore.QThread):

        def __init__(self, widget, **opts):
            QtCore.QThread.__init__(self)
            self.widget = widget
            self.config = opts

        def run(self):
            try:
                self.widget._info(u'Importing <b>%s</b> into <b>%s</b>...' %
                                  (self.config['url'], self.config['dest']))
                p = subprocess.Popen(['./hg', 'clone', self.config['url'],
                                     '--config', 'extensions.hgsubversion=../hgsubversion/',
                                     '--config', 'hgsubversion.defaulthost=atlassian.com',
                                     '--config', 'ui.interactive=off',
                                     self.config['dest']],
                                 cwd='./mercurial-1.8.1',
                                 env={'LD_LIBRARY_PATH': '.',
                                      'LC_ALL': 'en_US.UTF-8'},
                                 shell=False,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
                line = p.stdout.readline()
                while line:
                    self.widget._info(line)
                    line = p.stdout.readline()

                ret = p.wait()
                if ret:
                    self.widget._error(u'Failed: ' + str(ret))
                else:
                    self.widget._info(u'Done')

            except Exception:
                type_, message, tb = sys.exc_info()
                try:
                    self.widget._error(escape(u'%s: %s' % (str(type_), str(message))))
                    for frame in traceback.format_list(traceback.extract_tb(tb)):
                        self.widget._error(escape(frame))
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

    def initializePage(self):
        url         = str(QtGui.QWizardPage.field(self, 'url').toString())
        username    = str(QtGui.QWizardPage.field(self, 'username').toString())
        password    = str(QtGui.QWizardPage.field(self, 'password').toString())
        dest        = str(QtGui.QWizardPage.field(self, 'localDir').toString())

        try:
            job = WizardPage.Job(self, **{
                'url': url,
#                'url': 'file:///home/erik/work/repos/local-svn',
                'username': username,
                'password': password,
                'dest': dest,
#                'dest': sys.argv[1]
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
                traceback.print_exception(*sys.exc_info())

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
