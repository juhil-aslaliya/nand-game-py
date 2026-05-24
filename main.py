import sys
import os
from PySide6.QtWidgets import QApplication
from graphics.scene import CanvasScene
from graphics.view import CanvasView
from graphics.node_item import Node
from graphics.edge_item import Edge
from utils.serialization import save_to_file, load_from_file

SAVE_FILE = 'save_state.json'

def setup_default_scene(scene):
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

def main():
    app = QApplication(sys.argv)
    scene = CanvasScene()
    
    # Try to load existing state, otherwise use default
    if not load_from_file(scene, SAVE_FILE):
        setup_default_scene(scene)
        
    view = CanvasView(scene)
    view.setWindowTitle('Canvas UI')
    view.resize(1400, 900)
    view.show()
    
    # Auto-save when the application is about to quit
    app.aboutToQuit.connect(lambda: save_to_file(scene, SAVE_FILE))
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
