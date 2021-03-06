import sys
import urllib2
from PySide.QtGui import *

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        date = self.getDate()
        rates = sorted(self.rates.keys())

        self.setWindowTitle("Currency Converter")

        dateLabel = QLabel(date)
        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(rates)
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(.01, 1000000000.00)
        self.fromSpinBox.setValue(1.00)

        self.toComboBox = QComboBox()
        self.toComboBox.addItems(rates)
        self.toLabel = QLabel("1.00")

        grid = QGridLayout()
        grid.addWidget(dateLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)

        self.fromComboBox.currentIndexChanged.connect(self.updateUi)
        self.toComboBox.currentIndexChanged.connect(self.updateUi)
        self.fromSpinBox.valueChanged.connect(self.updateUi)

    def updateUi(self):
        fromCurrency = self.fromComboBox.currentText()
        toCurrency = self.toComboBox.currentText()

        amount = (self.rates[fromCurrency] / self.rates[toCurrency]) * self.fromSpinBox.value()
        self.toLabel.setText("%0.2f" % amount)

    def getDate(self):
        self.rates = {}

        try:
            date = "Unknown"

            fh = urllib2.urlopen("http://www.bankofcanada.ca/stats/assets/csv/fx-seven-day.csv")
            for line in fh:
                line = line.rstrip()
                if not line or line.startswith(("#", "Closing")):
                    continue

                fields = line.split(",")
                if line.startswith("Date "):
                    date = fields[-1]
                else:
                    try:
                        value = float(fields[-1])
                        self.rates[fields[0]] = value
                    except ValueError:
                        pass

            return "Exchange rates for " + date
        except Exception, e:
            return "Failed to download:\n%s" % e

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()