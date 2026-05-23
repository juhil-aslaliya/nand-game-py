from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen, QPainterPath
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsTextItem
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .scene import CanvasScene

class Port(QGraphicsPathItem):
    SIZE = 10
    INPUT = 'input'
    OUTPUT = 'output'
    def __init__(self, node, port_type, name=''):
        super().__init__()
        self.node = node
        self.port_type = port_type
        self.name = name
        self.edges = []
        self.setParentItem(node)
        self.setBrush(QColor(120, 170, 255))
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(2)
        self.setPen(pen)
        self.setPath(self.build_triangle())
        self.label = QGraphicsTextItem(name)
        self.label.setDefaultTextColor(Qt.GlobalColor.white)
        self.label.setParentItem(self)
    def build_triangle(self):
        r = self.SIZE
        path = QPainterPath()
        path.moveTo(-r, -r)
        path.lineTo(r, 0)
        path.lineTo(-r, r)
        path.closeSubpath()
        return path
    def connection_pos(self):
        pos = self.scenePos()
        r = self.SIZE
        if self.port_type == self.INPUT:
            return pos.x() - r, pos.y()
        return pos.x() + r, pos.y()
    def can_connect(self):
        if self.port_type == self.INPUT:
            return len(self.edges) == 0
        return True
    def add_edge(self, edge):
        if not self.can_connect():
            return False
        self.edges.append(edge)
        return True
    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
    def mousePressEvent(self, event):
        scene = cast('CanvasScene', self.scene())
        if self.port_type == self.OUTPUT:
            scene.start_edge_drag(self)
        event.accept()
    def mouseReleaseEvent(self, event):
        scene = cast('CanvasScene', self.scene())
        if self.port_type == self.INPUT and scene.dragging_edge:
            scene.finish_edge_drag(self)
        event.accept()
