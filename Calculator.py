import sys
from math import *
from PySide.QtGui import *

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.browser = QTextBrowser()
        self.lineEdit = QLineEdit("Type an expression and press Enter.")
        self.lineEdit.selectAll()

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

        self.lineEdit.setFocus()

        #OLD WAY self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.updateUi)
        self.lineEdit.returnPressed.connect(self.updateUi)

        self.setWindowTitle("Calculate")

    def updateUi(self):
        try:
            text = self.lineEdit.text()
            self.browser.append("%s = <b>%s</b>" % (text, eval(text)))
            self.lineEdit.selectAll()
        except:
            self.browser.append("<font color=red>%s is invalid</font>" % text)
            self.lineEdit.selectAll()

app = QApplication(sys.argv)
form = Form()
form.show()
form.exec_()