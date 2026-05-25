from PySide6.QtWidgets import QMainWindow, QSplitter
from PySide6.QtCore import Qt
from ui.sidebar import Sidebar
from graphics.view import CanvasView
from graphics.scene import CanvasScene
from graphics.node_item import Node
from utils.serialization import save_to_file, load_from_file
from core.evaluator import GraphEvaluator
import os

SAVE_FILE = 'save_state.json'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Canvas UI")
        self.resize(1400, 900)

        # Create scene and view
        self.scene = CanvasScene()
        
        # Load state or create defaults
        if not load_from_file(self.scene, SAVE_FILE):
            self.setup_default_scene()
            
        self.view = CanvasView(self.scene)

        # Create sidebar
        self.sidebar = Sidebar()
        self.pending_node_template = None
        self.sidebar.template_selected.connect(self.set_pending_node)
        self.view.canvas_clicked.connect(self.handle_canvas_click)
        self.sidebar.run_requested.connect(self.execute_graph)

        # Setup Splitter layout
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.view)
        
        # Remove the thick white band (handle) completely
        self.splitter.setHandleWidth(0)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setStyleSheet(
            "QSplitter { border: none; } "
            "QSplitter::handle { background: none; }"
        )
        
        from PySide6.QtWidgets import QFrame
        self.view.setFrameShape(QFrame.Shape.NoFrame)

        # Main window background color to prevent white flashes
        self.setStyleSheet("QMainWindow { background-color: #2b2b2b; }")
        
        # Make the canvas take up most of the space
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

        self.setCentralWidget(self.splitter)

    def setup_default_scene(self):
        from graphics.edge_item import Edge
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

        self.scene.addItem(node1)
        self.scene.addItem(node2)

        edge = Edge(
            node1.output_ports[0],
            node2.input_ports[0]
        )

        self.scene.addItem(edge)

    def set_pending_node(self, template_data):
        self.pending_node_template = template_data

    def handle_canvas_click(self, pos):
        if self.pending_node_template:
            node = Node(
                pos.x(),
                pos.y(),
                label=self.pending_node_template["name"],
                inputs=self.pending_node_template.get("inputs", []),
                outputs=self.pending_node_template.get("outputs", []),
                function=self.pending_node_template.get("function", "")
            )
            self.scene.addItem(node)
            
            # Reset state
            self.pending_node_template = None
            self.sidebar.template_list.clearSelection()

    def closeEvent(self, event):
        save_to_file(self.scene, SAVE_FILE)
        super().closeEvent(event)
    
    def execute_graph(self):
        GraphEvaluator.evaluate(self.scene)
