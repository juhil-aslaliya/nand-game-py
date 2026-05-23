from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QGraphicsView

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
