from PySide6.QtWidgets import QApplication
from ui.dialogs import CreateNodeDialog
import sys

app = QApplication(sys.argv)
dialog = CreateNodeDialog()
dialog.show()
sys.exit(0)
