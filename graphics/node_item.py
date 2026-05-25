import uuid
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen, QBrush, QFont
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem
from .port_item import Port

class Node(QGraphicsRectItem):
    MIN_WIDTH = 140
    SIDE_PADDING = 30
    PORT_TEXT_PADDING = 20
    TOP_PADDING = 40
    BOTTOM_PADDING = 20
    PORT_SPACING = 20
    GRID_SIZE = 10
    
    def __init__(self, x, y, label='Node', inputs=None, outputs=None, node_id=None, function=None, internal_graph=None):
        self.id = node_id or str(uuid.uuid4())
        self.inputs = inputs or []
        self.outputs = outputs or []
        self.function = function or ''
        self.internal_graph = internal_graph
        self.pin_state = False
        self.height = self.compute_height()
        super().__init__(0, 0, self.MIN_WIDTH, self.height)
        self.setPos(x, y)
        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(2)
        self.setPen(pen)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.label = QGraphicsTextItem(label)
        font = QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setDefaultTextColor(Qt.GlobalColor.white)
        self.label.setParentItem(self)
        self.label.setPos(10, 10)
        self.input_ports = []
        self.output_ports = []
        self.create_ports()
        self.update_layout()
        self.update_visuals()

    def compute_width(self):
        label_width = self.label.boundingRect().width()
        left_width = 0
        for port in self.input_ports:
            left_width = max(left_width, port.label.boundingRect().width())
        right_width = 0
        for port in self.output_ports:
            right_width = max(right_width, port.label.boundingRect().width())
        required_width = left_width + right_width + label_width + self.SIDE_PADDING * 4
        width = max(self.MIN_WIDTH, required_width)
        return round(width / self.GRID_SIZE) * self.GRID_SIZE

    def compute_height(self):
        rows = max(len(self.inputs), len(self.outputs), 1)
        height = self.TOP_PADDING + rows * self.PORT_SPACING + self.BOTTOM_PADDING
        return round(height / self.GRID_SIZE) * self.GRID_SIZE

    def create_ports(self):
        for name in self.inputs:
            port = Port(self, Port.INPUT, name)
            self.input_ports.append(port)
        for name in self.outputs:
            port = Port(self, Port.OUTPUT, name)
            self.output_ports.append(port)

    def update_layout(self):
        self.height = self.compute_height()
        self.width = self.compute_width()
        self.setRect(0, 0, self.width, self.height)
        for i, port in enumerate(self.input_ports):
            y = self.TOP_PADDING + i * self.PORT_SPACING
            port.setPos(0, y)
            port.label.setPos(15, -10)
        for i, port in enumerate(self.output_ports):
            y = self.TOP_PADDING + i * self.PORT_SPACING
            port.setPos(self.width, y)
            text_width = port.label.boundingRect().width()
            port.label.setPos(-text_width - 15, -10)
        label_rect = self.label.boundingRect()
        label_x = (self.width - label_rect.width()) / 2
        label_y = (self.TOP_PADDING - label_rect.height()) / 2
        self.label.setPos(label_x, label_y)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            x = round(value.x() / self.GRID_SIZE) * self.GRID_SIZE
            y = round(value.y() / self.GRID_SIZE) * self.GRID_SIZE
            return value.__class__(x, y)
        elif change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            ports = self.input_ports + self.output_ports
            for port in ports:
                for edge in port.edges:
                    edge.update_position()
        return super().itemChange(change, value)
    
    def update_visuals(self):
        label_text = self.label.toPlainText()
        if label_text in ["Input Pin", "Output Pin"]:
            color = QColor(65, 105, 225) if self.pin_state else QColor(85, 85, 85)
        else:
            color = QColor(120, 120, 120)
        self.setBrush(QBrush(color))

    def mouseDoubleClickEvent(self, event):
        if self.label.toPlainText() == "Input Pin":
            # Toggle the internal state
            self.pin_state = not self.pin_state
            
            port_name = self.output_ports[0].label.toPlainText() if self.output_ports else "Val"
            self.function = f"{port_name} = {self.pin_state}"
            # Repaint the node
            self.update_visuals()
            if hasattr(self.scene(), 'graph_changed'):
                self.scene().graph_changed.emit()
            
        super().mouseDoubleClickEvent(event)