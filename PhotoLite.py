from App.Config import *
from App.UI import PhotoLite_UI
import App.ImageEditing.Tools as Tools

import sys

from types import TracebackType
from typing import Optional, Type

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class PhotoLite(QMainWindow, PhotoLite_UI):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui(self)

        self.open_file_action.triggered.connect(self.image_area.open_image_file)

        self.rotate_left_action.triggered.connect(lambda: self.image_area.apply_filter(Tools.rotate_tool, 90))
        self.rotate_right_action.triggered.connect(lambda: self.image_area.apply_filter(Tools.rotate_tool, -90))
        
        self.zoom_in_action.triggered.connect(lambda: self.zoom_image(1.25))
        self.zoom_out_action.triggered.connect(lambda: self.zoom_image(0.8))

        self.about_action.triggered.connect(self.about_message)

        self.show()

    def zoom_image(self, ratio: float) -> None:
        zoom_value = self.image_area.resize_image(ratio)

        self.zoom_in_action.setEnabled(zoom_value < 3)
        self.zoom_out_action.setEnabled(zoom_value > 0.3)

    def about_message(self) -> None:
        QMessageBox.about(self, f'О {program_name}', about_description)
    
def except_hook(cls: Type[BaseException], exception: BaseException, traceback: Optional[TracebackType]) -> None:
    sys.__excepthook__(cls, exception, traceback)


def main() -> None:
    application = QApplication(sys.argv)

    application.setAttribute(Qt.AA_UseHighDpiPixmaps)
    application.setStyle('Fusion')  # type: ignore
    
    window = PhotoLite()

    sys.excepthook = except_hook
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
