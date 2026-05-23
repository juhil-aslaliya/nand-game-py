import sys
from PySide6.QtWidgets import QApplication
from graphics.scene import CanvasScene
from graphics.view import CanvasView
from graphics.node_item import Node
from graphics.edge_item import Edge


app = QApplication(sys.argv)
scene = CanvasScene()
node1 = Node(
    0,
    0,
    "Mathematics, we are actually checking its limits",
    inputs=["A", "B"],
    outputs=["Result"]
)

node2 = Node(
    400,
    200,
    "Display",
    inputs=["Value"],
    outputs=[]
)

scene.addItem(node1)
scene.addItem(node2)

edge = Edge(
    node1.output_ports[0],
    node2.input_ports[0]
)

scene.addItem(edge)
view = CanvasView(scene)
view.setWindowTitle('Canvas UI')
view.resize(1400, 900)
view.show()
sys.exit(app.exec())
        