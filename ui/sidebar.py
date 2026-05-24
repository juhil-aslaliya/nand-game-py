from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QPushButton, QListWidget, QLabel
)
from PySide6.QtCore import Signal
from utils.templates import load_templates, save_templates
from ui.dialogs import CreateNodeDialog


class Sidebar(QFrame):
    template_selected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(250)
        self.main_layout = QVBoxLayout(self)

        self.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                color: #e0e0e0;
                font-family: "Segoe UI", "Helvetica Neue", sans-serif;
                font-size: 14pt;
            }
            QPushButton {
                background-color: #3c3f41;
                color: white;
                border: 1px solid #555555;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4b4d4f;
            }
            QListWidget {
                background-color: #313335;
                border: 1px solid #555555;
                font-size: 13pt;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #2f65ca;
                color: white;
            }
            QLabel {
                font-weight: bold;
                margin-top: 10px;
                margin-bottom: 5px;
            }
        """)

        self.templates = load_templates()

        # Create button
        self.create_btn = QPushButton("Create New Node")
        self.create_btn.clicked.connect(self.open_create_dialog)
        self.main_layout.addWidget(self.create_btn)

        # Label
        self.main_layout.addWidget(QLabel("Saved Templates:"))

        # List widget
        self.template_list = QListWidget()
        self.template_list.itemClicked.connect(self.on_item_clicked)
        self.main_layout.addWidget(self.template_list)

        self.refresh_list()

    def refresh_list(self):
        self.template_list.clear()
        for t in self.templates:
            self.template_list.addItem(t["name"])

    def open_create_dialog(self):
        dialog = CreateNodeDialog(self)
        if dialog.exec():
            data = dialog.get_template_data()
            self.templates.append(data)
            save_templates(self.templates)
            self.refresh_list()

    def on_item_clicked(self, item):
        name = item.text()
        for t in self.templates:
            if t["name"] == name:
                self.template_selected.emit(t)
                break
