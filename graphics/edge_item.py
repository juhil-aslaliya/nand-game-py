from PySide6.QtGui import QColor, QPen, QPainterPath
from PySide6.QtWidgets import QGraphicsPathItem

class Edge(QGraphicsPathItem):
    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item.output_port
        self.end_item = end_item.input_port
        self.start_item.edges.append(self)
        self.end_item.edges.append(self)
        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(3)
        self.setPen(pen)
        self.update_position()
    def update_position(self):
        start = self.start_item.sceneBoundingRect().center()
        end = self.end_item.sceneBoundingRect().center()
        path = QPainterPath()
        path.moveTo(start)
        dx = (end.x() - start.x()) * 0.5
        path.cubicTo(start.x()+dx, start.y(), end.x()-dx, end.y(), end.x(), end.y())
        self.setPath(path)
