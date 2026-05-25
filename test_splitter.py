import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

app = QApplication(sys.argv)
window = QMainWindow()

splitter = QSplitter(Qt.Orientation.Horizontal)
w1 = QWidget()
w1.setStyleSheet("background-color: #2b2b2b;")
w1.setFixedWidth(250)

w2 = QFrame()
w2.setStyleSheet("background-color: #303030;")

splitter.addWidget(w1)
splitter.addWidget(w2)

splitter.setHandleWidth(0)
splitter.setStyleSheet("QSplitter::handle { background-color: transparent; }")

window.setCentralWidget(splitter)
window.show()
sys.exit(0)
