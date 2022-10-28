import os

from App.Config import *

from typing import Union

from dataclasses import dataclass
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import (QMainWindow, QLabel, QSizePolicy, QScrollArea,
                             QToolBar, QAction, QMenuBar, QFileDialog)


@dataclass()
class Action:
    name: str
    text: str
    shortcut: str
    location: Union[QToolBar, QMenuBar]


actions_list = (
    Action('open_file', 'Открыть изображение', 'Ctrl+O', QToolBar),
    Action('zoom_in', 'Приблизить', 'Ctrl+=', QToolBar),
    Action('zoom_out', 'Отдалить', 'Ctrl+-', QToolBar)
)


class ImageArea(QLabel):
    def __init__(self, main_window: QMainWindow) -> None:
        super().__init__(main_window)

        self.main_window = main_window
        self.image = QImage()

        self.zoom_value = 1

        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setScaledContents(True)

        self.setPixmap(QPixmap().fromImage(self.image))
        self.setAlignment(Qt.AlignCenter)

    def _set_image(self, path: str) -> None:
        self.image = QImage(path)
        self.setPixmap(QPixmap().fromImage(self.image))
        self.resize(self.image.size())

        self.zoom_value = 1

    def resize_image(self, ratio: float) -> float:
        self.zoom_value = round(self.zoom_value * ratio, 2)

        size = self.image.size()
        width, height = size.width() * self.zoom_value, size.height() * self.zoom_value
        self.resize(QSize(width, height))

        return self.zoom_value

    def open_image_file(self):
        image_path = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '', f'Изображение ({"; ".join(image_formats)})')[0]
        
        if image_path:
            self._set_image(image_path)


class PhotoLite_UI(object):
    def init_ui(self, main_window: QMainWindow) -> None:
        main_window.setWindowTitle('PhotoLite')
        main_window.setMinimumSize(500, 500)

        main_window.showMaximized()

        self._init_main_area(main_window)
        self._init_actions(main_window)

    def _init_main_area(self, main_window: QMainWindow) -> None:
        self.image_area = ImageArea(main_window)
        self.scroll_area = QScrollArea()
        self.scroll_area.setAlignment(Qt.AlignCenter)

        self.scroll_area.setWidget(self.image_area)

        main_window.setCentralWidget(self.scroll_area)

    def _init_actions(self, main_window: QMainWindow) -> None:
        self.tool_bar = QToolBar('Инструменты')
        self.tool_bar.setIconSize(QSize(26, 26))

        for action in actions_list:
            icon_path = fr'App\Icons\{action.name}.svg'

            if os.path.isfile(icon_path):  
                q_action = QAction(QIcon(icon_path), action.text, main_window)
            else:
                q_action = QAction(action.text, main_window)

            q_action.setShortcut(action.shortcut)

            if action.location is QToolBar:
                self.tool_bar.addAction(q_action)

            setattr(self, action.name + '_action', q_action)

        main_window.addToolBar(Qt.LeftToolBarArea, self.tool_bar)


if __name__ == '__main__':
    pass
