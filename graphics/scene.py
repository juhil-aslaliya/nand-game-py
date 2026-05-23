from PySide6.QtWidgets import QGraphicsScene
from .edge_item import Edge, TemporaryEdge

class CanvasScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.dragging_edge = None
        self.drag_start_port = None
    def start_edge_drag(self, port):
        self.drag_start_port = port
        self.dragging_edge = TemporaryEdge(port)
        self.addItem(self.dragging_edge)
    def finish_edge_drag(self, input_port):
        if self.drag_start_port and input_port.can_connect():
            edge = Edge(self.drag_start_port, input_port)
            self.addItem(edge)
        self.cancel_edge_drag()
    def cancel_edge_drag(self):
        if self.dragging_edge:
            self.removeItem(self.dragging_edge)
            self.dragging_edge = None
        self.drag_start_port = None
    def mouseMoveEvent(self, event):
        if self.dragging_edge:
            self.dragging_edge.set_target(event.scenePos())
        return super().mouseMoveEvent(event)