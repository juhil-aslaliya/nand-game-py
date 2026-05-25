from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QGraphicsView, QGraphicsScene, QLabel, QTextEdit,
    QGraphicsItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from graphics.node_item import Node
from graphics.port_item import Port


class EditableNode(Node):
    def __init__(self, x, y, label='New Node', inputs=None, outputs=None):
        if inputs is None:
            inputs = ["A", "B"]
        if outputs is None:
            outputs = ["Result"]
        super().__init__(
            x, y, label=label, inputs=inputs, outputs=outputs
        )
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)

        flag = Qt.TextInteractionFlag.TextEditorInteraction
        self.label.setTextInteractionFlags(flag)
        self.label.document().contentsChanged.connect(self.update_layout)

        for port in self.input_ports + self.output_ports:
            port.label.setTextInteractionFlags(flag)
            port.label.document().contentsChanged.connect(self.update_layout)

    def add_input(self):
        port = Port(self, Port.INPUT, f"In {len(self.input_ports) + 1}")
        flag = Qt.TextInteractionFlag.TextEditorInteraction
        port.label.setTextInteractionFlags(flag)
        port.label.document().contentsChanged.connect(self.update_layout)
        self.input_ports.append(port)
        self.update_layout()

    def remove_input(self):
        if self.input_ports:
            port = self.input_ports.pop()
            self.scene().removeItem(port)
            self.update_layout()

    def add_output(self):
        port = Port(self, Port.OUTPUT, f"Out {len(self.output_ports) + 1}")
        flag = Qt.TextInteractionFlag.TextEditorInteraction
        port.label.setTextInteractionFlags(flag)
        port.label.document().contentsChanged.connect(self.update_layout)
        self.output_ports.append(port)
        self.update_layout()

    def remove_output(self):
        if self.output_ports:
            port = self.output_ports.pop()
            self.scene().removeItem(port)
            self.update_layout()

    def update_layout(self):
        super().update_layout()
        # Center the node around 0,0 dynamically
        self.setPos(-self.width / 2, -self.height / 2)

    def get_template_data(self):
        return {
            "name": self.label.toPlainText().strip() or "Untitled Node",
            "inputs": [
                p.label.toPlainText().strip() for p in self.input_ports
            ],
            "outputs": [
                p.label.toPlainText().strip() for p in self.output_ports
            ]
        }


class CreateNodeDialog(QDialog):
    def __init__(self, parent=None, template_data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Node Template" if template_data else "Create New Node Template")
        self.resize(600, 600)

        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3c3f41;
                color: white;
                border: 1px solid #555555;
                padding: 6px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4b4d4f;
            }
            QGraphicsView {
                border: 1px solid #555555;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #555555;
                font-family: monospace;
            }
        """)

        layout = QVBoxLayout(self)

        # Instruction Label
        instruction_text = (
            "Edit text directly on the node. "
            "Use buttons to add/remove ports."
        )
        instruction = QLabel(instruction_text)
        instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instruction)

        # Graphics View
        self.scene = QGraphicsScene()
        from PySide6.QtGui import QBrush, QColor
        self.scene.setBackgroundBrush(QBrush(QColor("#1e1e1e")))
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout.addWidget(self.view)

        # Setup Node
        label = template_data.get("name", "New Node") if template_data else "New Node"
        inputs = template_data.get("inputs") if template_data else None
        outputs = template_data.get("outputs") if template_data else None
        
        self.node = EditableNode(0, 0, label=label, inputs=inputs, outputs=outputs)
        self.scene.addItem(self.node)

        # Center the node
        self.view.setSceneRect(-300, -200, 600, 400)

        # Function Edit
        layout.addWidget(QLabel("Node Function (Python/Logic code):"))
        self.function_edit = QTextEdit()
        self.function_edit.setMaximumHeight(80)
        if template_data and "function" in template_data:
            self.function_edit.setPlainText(template_data["function"])
        layout.addWidget(self.function_edit)

        # Controls
        controls_layout = QHBoxLayout()

        # Input controls
        in_layout = QVBoxLayout()
        add_in_btn = QPushButton("+ Input")
        add_in_btn.clicked.connect(self.node.add_input)
        rm_in_btn = QPushButton("- Input")
        rm_in_btn.clicked.connect(self.node.remove_input)
        in_layout.addWidget(add_in_btn)
        in_layout.addWidget(rm_in_btn)
        controls_layout.addLayout(in_layout)

        # Output controls
        out_layout = QVBoxLayout()
        add_out_btn = QPushButton("+ Output")
        add_out_btn.clicked.connect(self.node.add_output)
        rm_out_btn = QPushButton("- Output")
        rm_out_btn.clicked.connect(self.node.remove_output)
        out_layout.addWidget(add_out_btn)
        out_layout.addWidget(rm_out_btn)
        controls_layout.addLayout(out_layout)

        layout.addLayout(controls_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.create_button = QPushButton("Save" if template_data else "Create")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.create_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_template_data(self):
        data = self.node.get_template_data()
        data["function"] = self.function_edit.toPlainText().strip()
        return data
