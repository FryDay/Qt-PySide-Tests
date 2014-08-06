import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *

app = QApplication(sys.argv)

try:
    due = QTime.currentTime()
    message = "Alert!"

    if len(sys.argv) < 2:
        raise ValueError

    hours, minutes = sys.argv[1].split(":")

    due = QTime(int(hours), int(minutes))

    if not due.isValid():
        raise ValueError

    if len(sys.argv) > 2:
        message = " ".join(sys.argv[2:])
except ValueError:
    message = "Usage = Alarm_Pop.py HH:MM [optional message]" #24 hour clock

while QTime.currentTime() < due:
    time.sleep(10)

label = QLabel("<font color=red size=72><br>" + message + "</br></font>")
label.setWindowFlags(Qt.SplashScreen)
label.show()

QTimer.singleShot(20000, app.quit) #20 seconds

app.exec_()