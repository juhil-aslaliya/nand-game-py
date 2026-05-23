from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QGraphicsEllipseItem

class Port(QGraphicsEllipseItem):
    RADIUS = 8
    INPUT = 0
    OUTPUT = 1
    def __init__(self, parent_node, port_type):
        super().__init__(QRectF(-self.RADIUS, -self.RADIUS, self.RADIUS*2, self.RADIUS*2))
        self.node = parent_node
        self.port_type = port_type
        self.edges = []
        if port_type == self.INPUT:
            self.setBrush(QColor(220, 120, 120))
        else:
            self.setBrush(QColor(120, 120, 220))
        self.setPen(QPen(Qt.GlobalColor.black))
        self.setParentItem(parent_node)
