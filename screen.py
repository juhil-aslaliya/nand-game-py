import sys
from PySide6.QtCore import QRect, Qt, QRectF
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPainterPath
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPathItem, QGraphicsEllipseItem, QGraphicsTextItem

class CanvasView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinMaxButtonsHint | Qt.WindowType.WindowCloseButtonHint)
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setSceneRect(-10000, -10000, 20000, 20000)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setBackgroundBrush(QColor(30, 30, 30))
        self.zoom = 1.0
    def wheelEvent(self, event):
        if event.modifiers() and Qt.KeyboardModifier.ControlModifier:
            zoom_in = 1.05
            zoom_out = 0.95
            old_zoom = self.zoom
            if event.angleDelta().y() > 0:
                factor = zoom_in
            else:
                factor = zoom_out
            new_zoom = old_zoom * factor
            min_zoom = 0.05
            max_zoom = 20
            if min_zoom <= new_zoom < max_zoom:
                self.zoom = new_zoom
                self.scale(factor, factor)
            return        
        delta = event.angleDelta()
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        grid_size = 50
        left = int(rect.left()) - (int(rect.left())%grid_size)
        top = int(rect.top()) - (int(rect.top())%grid_size)
        lines = []
        pen = QPen(QColor(50, 50, 50))
        pen.setWidth(1)
        painter.setPen(pen)
        x = left
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())  # type: ignore
            x += grid_size
        y = top
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y) # type: ignore
            y += grid_size

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


app = QApplication(sys.argv)
scene = QGraphicsScene()
node1 = Node(0, 0, 'Input')
node2 = Node(300, 100, 'Process')
edge = Edge(node1, node2)
scene.addItem(edge)
scene.addItem(node1)
scene.addItem(node2)
scene.addItem(Node(-200, -150))
scene.addItem(Node(500, -250))
view = CanvasView(scene)
view.setWindowTitle('Canvas UI')
view.resize(1400, 900)
view.show()
sys.exit(app.exec())
        