from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class CreateNodeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Node Template")
        
        self.layout = QVBoxLayout(self)
        
        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Node Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. AND Gate")
        name_layout.addWidget(self.name_input)
        self.layout.addLayout(name_layout)
        
        # Inputs
        inputs_layout = QHBoxLayout()
        inputs_layout.addWidget(QLabel("Inputs (comma separated):"))
        self.inputs_input = QLineEdit()
        self.inputs_input.setPlaceholderText("e.g. A, B")
        inputs_layout.addWidget(self.inputs_input)
        self.layout.addLayout(inputs_layout)
        
        # Outputs
        outputs_layout = QHBoxLayout()
        outputs_layout.addWidget(QLabel("Outputs (comma separated):"))
        self.outputs_input = QLineEdit()
        self.outputs_input.setPlaceholderText("e.g. Result")
        outputs_layout.addWidget(self.outputs_input)
        self.layout.addLayout(outputs_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.create_button = QPushButton("Create")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(button_layout)
        
        self.create_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_template_data(self):
        name = self.name_input.text().strip() or "Untitled Node"
        
        inputs_text = self.inputs_input.text()
        inputs = [i.strip() for i in inputs_text.split(',')] if inputs_text.strip() else []
        
        outputs_text = self.outputs_input.text()
        outputs = [o.strip() for o in outputs_text.split(',')] if outputs_text.strip() else []
        
        return {
            "name": name,
            "inputs": inputs,
            "outputs": outputs
        }
