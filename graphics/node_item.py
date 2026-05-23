from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen, QBrush
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from .port_item import Port

class Node(QGraphicsRectItem):
    def __init__(self, x, y, label='Node', w=180, h=100):
        self.WIDTH = w
        self.HEIGHT = h
        super().__init__(0, 0, self.WIDTH, self.HEIGHT)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor(70, 120, 220)))
        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(2)
        self.setPen(pen)
        self.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.label = QGraphicsTextItem(label)
        self.label.setDefaultTextColor(Qt.GlobalColor.white)
        self.label.setParentItem(self)
        self.label.setPos(10, 10)
        self.input_port = Port(self, Port.INPUT)
        self.output_port = Port(self, Port.OUTPUT)
        self.input_port.setPos(0, self.HEIGHT/2)
        self.output_port.setPos(self.WIDTH, self.HEIGHT/2)
    def itemChange(self, change, value):
        if change == QGraphicsRectItem.GraphicsItemChange.ItemPositionChange:
            ports = [self.input_port, self.output_port]
            for port in ports:
                for edge in port.edges:
                    edge.update_position()
        return super().itemChange(change, value)
