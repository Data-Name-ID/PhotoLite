from .ImageArea import *

import os

from typing import Type, Union, Tuple
from dataclasses import dataclass

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QScrollArea, QMenuBar,
                             QToolBar, QAction)


@dataclass()
class Action:
    name: str
    text: str
    shortcut: str
    location: Union[Type[QToolBar], Type[QMenuBar]]
    separator: bool = False


actions_list: Tuple[Action, ...] = (
    Action('open_file', 'Открыть изображение', 'Ctrl+O', QToolBar, True),
    Action('zoom_in', 'Приблизить', 'Ctrl+=', QToolBar),
    Action('zoom_out', 'Отдалить', 'Ctrl+-', QToolBar),
    Action('rotate_right', 'Повенуть на 90° по ч. с.', ']', QToolBar),
    Action('rotate_left', 'Повенуть на 90° против ч. с.', '[', QToolBar),
    Action('about', 'О программе', 'Ctrl+I', QMenuBar)
)


class PhotoLite_UI(object):
    def init_ui(self, main_window: QMainWindow) -> None:
        main_window.setWindowTitle(program_name)
        main_window.setMinimumSize(1000, 800)

        main_window.showMaximized()

        self._init_main_area(main_window)
        self._init_toolbar(main_window)
        self._init_actions(main_window)
        self._init_menubar(main_window)


    def _init_main_area(self, main_window: QMainWindow) -> None:
        self.image_area = ImageArea()
        self.scroll_area = QScrollArea(main_window)
        self.scroll_area.setAlignment(Qt.AlignCenter)

        self.scroll_area.setWidget(self.image_area)

        main_window.setCentralWidget(self.scroll_area)

    def _init_toolbar(self, main_window: QMainWindow) -> None:
        self.toolbar = QToolBar('Инструменты')
        self.toolbar.setIconSize(QSize(26, 26))
        main_window.addToolBar(Qt.LeftToolBarArea, self.toolbar)

    def _init_actions(self, main_window: QMainWindow) -> None:
        self.open_file_action: QAction
        self.zoom_in_action: QAction
        self.zoom_out_action: QAction
        self.rotate_right_action: QAction
        self.rotate_left_action: QAction
        self.about_action: QAction

        for action in actions_list:
            icon_path = fr'App\Icons\{action.name}.svg'

            if os.path.isfile(icon_path):  
                q_action = QAction(QIcon(icon_path), action.text, main_window)
            else:
                q_action = QAction(action.text, main_window)

            q_action.setShortcut(action.shortcut)

            if action.location is QToolBar:
                self.toolbar.addAction(q_action)

                if action.separator:
                    self.toolbar.addSeparator()

            setattr(self, action.name + '_action', q_action)


    def _init_menubar(self, main_window: QMainWindow) -> None:
        self.menubar = main_window.menuBar()

        self.file_menu = self.menubar.addMenu('Файл')
        self.file_menu.addAction(self.open_file_action)

        self.edit_menu = self.menubar.addMenu('Редактирование')
        self.edit_menu.addSection('Трансформирование')
        self.edit_menu.addAction(self.rotate_right_action)
        self.edit_menu.addAction(self.rotate_left_action)

        self.help_menu = self.menubar.addMenu('Справка')
        self.help_menu.addAction(self.about_action)


if __name__ == '__main__':
    pass
