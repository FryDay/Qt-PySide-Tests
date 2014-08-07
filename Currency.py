import sys
import urllib2
from functools import partial
from PySide.QtCore import *
from PySide.QtGui import *

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        date = self.getData()
        rates = sorted(self.rates.keys())

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

        self.fromComboBox.currentIndexChanged.connect(partial(self.updateUi, self.fromComboBox.currentIndex()))
        self.toComboBox.currentIndexChanged.connect(partial(self.updateUi, self.toComboBox.currentIndex()))
        self.fromSpinBox.valueChanged.connect(partial(self.updateUi, self.fromSpinBox.value()))

    def updateUi(self):
        to = self.toComboBox.currentText()
        from_ = self.fromComboBox.currentText()

        amount = (self.rates[from_] / self.rates[to]) * self.fromSpinBox.value()
        self.toLabel.setText("%0.2f" % amount)

    def getDate(self):
        self.rates = {}

        try:
            date = "Unknown"

            fh = urllib2.urlopen("http://www.bankofcanada.ca/stats/assets/csv/fx-seven-day.csv")
            for line in fh:
                line = line.rstrip()
                if not line or line.startswith("#", "Closing"):
                    continue

                field = line.split(",")

        except: