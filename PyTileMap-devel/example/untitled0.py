import sys

from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter, QColor, QPen, QBrush, QPixmap
from qtpy.QtWidgets import QMainWindow, QGraphicsView, QGraphicsItem, \
    QGraphicsSimpleTextItem, QApplication

from pytilemap import MapGraphicsView, MapTileSourceHere, MapTileSourceOSM
class MapZoom(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        view = MapGraphicsView(tileSource=MapTileSourceHere())

        self.setCentralWidget(view)
        view.scene().setCenter(31.789339, 41.450508)
        view.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        view.setRenderHint(QPainter.Antialiasing, True)
        view.setRenderHint(QPainter.SmoothPixmapTransform, True)
        pointItem = view.scene().addCircle(31.789339, 44.860767, 3.0)
        pointItem.setBrush(Qt.black)
        pointItem.setToolTip('31.789339, 41.450508')
        pointItem.setFlag(QGraphicsItem.ItemIsSelectable, True)
        pointItem = view.scene().addCircle(31.789339, 44.860767, 5.0)
        pointItem.setBrush(Qt.green)
        pointItem.setPen(QPen(Qt.NoPen))
        pointItem.setToolTip('%f, %f' % (31.789339, 44.860767))
        pointItem.setFlag(QGraphicsItem.ItemIsSelectable, True)
        lineItem = view.scene().addLine(32.859741, 39.933365,31.789339,41.450508)
        lineItem.setPen(QPen(QBrush(Qt.blue), 3.0))
        
        polylineItem = view.scene().addPolyline('41.450508', '31.789339')
        polylineItem.setPen(QPen(QBrush(Qt.red), 3.0))
        pix = QPixmap(24, 24)
        pix.fill(Qt.red)
        pixmapItem = view.scene().addPixmap(31.789339, 44.860767, pix)
        pixmapItem.setOffset(-12, -12)
        
        
        
        
        
        
def main():
    w = MapZoom()
    w.setWindowTitle("OpenStreetMap")

    w.resize(800, 600)
    w.show()

    return app.exec_()

if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("TileMap")

    sys.exit(main())