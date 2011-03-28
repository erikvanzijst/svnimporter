__author__ = 'erik'

import tempfile
from PyQt4 import QtGui

class WizardPage(QtGui.QWizardPage):

    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)

        grid = QtGui.QGridLayout()

        description = QtGui.QLabel('Specify username mappings below, or provide a mapping file.')
        grid.addWidget(description, 0, 0)

        self.text = QtGui.QPlainTextEdit(parent=self)
        self.text.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        grid.addWidget(self.text, 1, 0)


        self.setLayout(grid)

    def initializePage(self):
        if self.text.toPlainText().size() == 0:
            self.text.setPlainText(
'''# Author mappings must be provided one per line and formatted
# as per the example below. Lines starting with '#' are ignored.
#
# Example:
# jdoe = John Doe <jdoe@acme.org>
''')

    def validatePage(self):
        # save the mapping file and proceed
        filename = tempfile.mktemp(prefix='svnimporter_authorfile_')
        with open(filename, 'w') as f:
            f.write(str(self.text.toPlainText()))

        self.wizard().authorfile = filename
        print self.wizard().authorfile
        return True
        