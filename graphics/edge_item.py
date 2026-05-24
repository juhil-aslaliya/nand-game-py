from PySide6.QtGui import QColor, QPen, QPainterPath
from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtCore import QPointF
from .port_item import Port

class Edge(QGraphicsPathItem):
    def __init__(self, output_port, input_port):
        super().__init__()
        if output_port.port_type != Port.OUTPUT:
            raise ValueError('Start port must be OUTPUT')
        if input_port.port_type != Port.INPUT:
            raise ValueError('End port must be INPUT')
        if not input_port.can_connect():
            raise ValueError('Input port already occupied')
        self.output_port = output_port
        self.input_port = input_port
        output_port.add_edge(self)
        input_port.add_edge(self)
        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(3)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        self.setPen(pen)
        self.setZValue(-10)
        self.update_position()
    def update_position(self):
        start_x, start_y = self.output_port.connection_pos()
        end_x, end_y = self.input_port.connection_pos()
        path = QPainterPath()
        path.moveTo(start_x, start_y)
        dx = end_x - start_x
        dy = end_y - start_y
        diag = min(abs(dx), abs(dy))
        diag_dx = diag if dx >= 0 else -diag
        diag_dy = diag if dy >= 0 else -diag
        diag_end_x = start_x + diag_dx
        diag_end_y = start_y + diag_dy
        path.lineTo(diag_end_x, diag_end_y)
        path.lineTo(end_x, end_y)
        self.setPath(path)

    def paint(self, painter, option, widget=None):
        if self.isSelected():
            pen = QPen(QColor(255, 200, 0))
            pen.setWidth(6)
            painter.setPen(pen)
        else:
            painter.setPen(self.pen())
        painter.setBrush(self.brush())
        painter.drawPath(self.path())

class TemporaryEdge(QGraphicsPathItem):
    def __init__(self, start_port):
        super().__init__()
        self.start_port = start_port
        pen = QPen(QColor(180, 180, 180))
        pen.setWidth(2)
        self.setPen(pen)
        self.target_pos = QPointF()
    def set_target(self, pos):
        self.target_pos = pos
        self.update_position()
    def update_position(self):
        start_x, start_y = self.start_port.connection_pos()
        end_x = self.target_pos.x()
        end_y = self.target_pos.y()
        path = QPainterPath()
        path.moveTo(start_x, start_y)
        path.lineTo(end_x, end_y)
        self.setPath(path)