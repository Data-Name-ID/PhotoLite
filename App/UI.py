import os

from App.Config import image_formats

from typing import Type, Union

from dataclasses import dataclass
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import (QMainWindow, QLabel, QScrollArea, QMenuBar,
                             QToolBar, QAction, QFileDialog)


@dataclass()
class Action:
    name: str
    text: str
    shortcut: str
    location: Union[Type[QToolBar], Type[QMenuBar]]


actions_list = (
    Action('open_file', 'Открыть изображение', 'Ctrl+O', QToolBar),
    Action('zoom_in', 'Приблизить', 'Ctrl+=', QToolBar),
    Action('zoom_out', 'Отдалить', 'Ctrl+-', QToolBar),
    Action('about', 'О программе', '', QMenuBar)
)


class ImageArea(QLabel):
    def __init__(self, main_window: QMainWindow) -> None:
        super().__init__(main_window)

        self.main_window = main_window

        self.zoom_value = 1.0
        
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignCenter)

    def _set_image(self, path: str) -> None:
        self.image = QImage(path)
        self.setPixmap(QPixmap().fromImage(self.image))
        self.resize(self.image.size())

        self.zoom_value = 1

    def resize_image(self, ratio: float) -> float:
        self.zoom_value = round(self.zoom_value * ratio, 2)

        size = self.image.size()
        width, height = int(size.width() * self.zoom_value), int(size.height() * self.zoom_value)
        self.resize(QSize(width, height))

        return self.zoom_value

    def open_image_file(self) -> None:
        image_path = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '', f'Изображение ({"; ".join(image_formats)})')[0]
        
        if image_path:
            self._set_image(image_path)


class PhotoLite_UI(object):
    def init_ui(self, main_window: QMainWindow) -> None:
        main_window.setWindowTitle('PhotoLite')
        main_window.setMinimumSize(500, 500)

        main_window.showMaximized()

        self._init_main_area(main_window)
        self._init_toolbar(main_window)
        self._init_actions(main_window)
        self._init_menubar(main_window)


    def _init_main_area(self, main_window: QMainWindow) -> None:
        self.image_area = ImageArea(main_window)
        self.scroll_area = QScrollArea(main_window)
        self.scroll_area.setAlignment(Qt.AlignCenter)

        self.scroll_area.setWidget(self.image_area)

        main_window.setCentralWidget(self.scroll_area)

    def _init_toolbar(self, main_window: QMainWindow) -> None:
        self.toolbar = QToolBar('Инструменты')
        self.toolbar.setIconSize(QSize(26, 26))
        main_window.addToolBar(Qt.LeftToolBarArea, self.toolbar)

    def _init_actions(self, main_window: QMainWindow) -> None:
        for action in actions_list:
            icon_path = fr'App\Icons\{action.name}.svg'

            if os.path.isfile(icon_path):  
                q_action = QAction(QIcon(icon_path), action.text, main_window)
            else:
                q_action = QAction(action.text, main_window)

            q_action.setShortcut(action.shortcut)

            if action.location is QToolBar:
                self.toolbar.addAction(q_action)

            setattr(self, action.name + '_action', q_action)

    def _init_menubar(self, main_window: QMainWindow) -> None:
        self.menubar = main_window.menuBar()

        self.file_menu = self.menubar.addMenu('Файл')
        self.file_menu.addAction(self.open_file_action)

        self.help_menu = self.menubar.addMenu('Справка')
        self.help_menu.addAction(self.about_action)


if __name__ == '__main__':
    pass
