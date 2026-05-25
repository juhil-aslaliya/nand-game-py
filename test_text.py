from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsTextItem
import sys

app = QApplication(sys.argv)
scene = QGraphicsScene()
text = QGraphicsTextItem("Editable")
from PySide6.QtCore import Qt
text.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
scene.addItem(text)
view = QGraphicsView(scene)
view.show()
sys.exit(0)
