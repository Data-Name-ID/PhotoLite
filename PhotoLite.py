import sys

from App.UI import PhotoLite_UI
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow


class PhotoLite(QMainWindow, PhotoLite_UI):
    def __init__(self):
        super().__init__()
        self.init_ui(self)

        self.open_file_action.triggered.connect(self.image_area.open_image_file)
        
        self.zoom_in_action.triggered.connect(lambda: self.zoom_image(1.25))
        self.zoom_out_action.triggered.connect(lambda: self.zoom_image(0.8))

        self.show()

    def zoom_image(self, ratio: float):
        zoom_value = self.image_area.resize_image(ratio)

        self.zoom_in_action.setEnabled(zoom_value < 3)
        self.zoom_out_action.setEnabled(zoom_value > 0.3)

    
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QApplication(sys.argv)

    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setStyle('Fusion')
    
    window = PhotoLite()

    sys.excepthook = except_hook
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
