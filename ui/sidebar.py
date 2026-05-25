from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QPushButton, QListWidget, QLabel
)
from PySide6.QtCore import Signal
from utils.templates import load_templates, save_templates
from ui.dialogs import CreateNodeDialog


class Sidebar(QFrame):
    template_selected = Signal(dict)
    run_requested = Signal()

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

        self.run_btn = QPushButton("Run")
        self.run_btn.setStyleSheet("background-color: #2a82da; color: white;")
        self.run_btn.clicked.connect(self.run_requested.emit)
        self.main_layout.addWidget(self.run_btn)


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

        # Edit button
        self.edit_btn = QPushButton("Edit Selected Template")
        self.edit_btn.clicked.connect(self.edit_selected_template)
        self.main_layout.addWidget(self.edit_btn)

        # Delete button
        self.delete_btn = QPushButton("Delete Selected Template")
        self.delete_btn.clicked.connect(self.delete_selected_template)
        self.main_layout.addWidget(self.delete_btn)

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

    def delete_selected_template(self):
        selected_items = self.template_list.selectedItems()
        if not selected_items:
            return
        
        name = selected_items[0].text()
        
        for t in self.templates:
            if t["name"] == name:
                self.templates.remove(t)
                break
                
        save_templates(self.templates)
        self.refresh_list()

    def edit_selected_template(self):
        selected_items = self.template_list.selectedItems()
        if not selected_items:
            return
        
        name = selected_items[0].text()
        
        for i, t in enumerate(self.templates):
            if t["name"] == name:
                dialog = CreateNodeDialog(self, template_data=t)
                if dialog.exec():
                    self.templates[i] = dialog.get_template_data()
                    save_templates(self.templates)
                    self.refresh_list()
                break