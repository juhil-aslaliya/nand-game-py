import sys
from PySide6.QtWidgets import QApplication
from graphics.scene import CanvasScene
from graphics.view import CanvasView
from graphics.node_item import Node
from graphics.edge_item import Edge


app = QApplication(sys.argv)
scene = CanvasScene()
node1 = Node(0, 0, 'Input')
node2 = Node(300, 100, 'Process')
edge = Edge(node1, node2)
scene.addItem(edge)
scene.addItem(node1)
scene.addItem(node2)
scene.addItem(Node(-200, -150))
scene.addItem(Node(500, -250))
view = CanvasView(scene)
view.setWindowTitle('Canvas UI')
view.resize(1400, 900)
view.show()
sys.exit(app.exec())
        