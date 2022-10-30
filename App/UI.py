import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QScrollArea,
                             QToolBar, QAction)

from .ImageArea import ImageArea
from .Config import actions_list, program_name


class PhotoLiteUI(object):
    def init_ui(self, main_window: QMainWindow) -> None:
        main_window.setWindowTitle(program_name)
        main_window.setWindowIcon(QIcon('App/Icons/PhotoLite.svg'))
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
        self.close_file_action: QAction

        self.save_file_action: QAction
        self.save_as_file_action: QAction

        self.step_forward_action: QAction
        self.step_back_action: QAction

        self.rotate_right_action: QAction
        self.rotate_left_action: QAction

        self.zoom_in_action: QAction
        self.zoom_out_action: QAction

        self.black_white_action: QAction

        self.about_action: QAction

        for action in actions_list:
            icon_path = f'App/Icons/Heroicons UI/{action.name}.svg'

            if os.path.isfile(icon_path):
                q_action = QAction(QIcon(icon_path), action.text, main_window)
            else:
                q_action = QAction(action.text, main_window)

            q_action.setShortcut(action.shortcut)
            q_action.setEnabled(action.enabled)

            if action.location is QToolBar:
                self.toolbar.addAction(q_action)

                if action.separator:
                    self.toolbar.addSeparator()

            setattr(self, action.name + '_action', q_action)

    def _init_menubar(self, main_window: QMainWindow) -> None:
        self.menubar = main_window.menuBar()

        self.file_menu = self.menubar.addMenu('Файл')
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.close_file_action)

        self.file_menu.addSection('Сохранение')
        self.file_menu.addAction(self.save_file_action)
        self.file_menu.addAction(self.save_as_file_action)

        self.edit_menu = self.menubar.addMenu('Редактирование')

        self.edit_menu.addSection('Действия')
        self.edit_menu.addAction(self.step_forward_action)
        self.edit_menu.addAction(self.step_back_action)

        self.edit_menu.addSection('Трансформирование')
        self.edit_menu.addAction(self.rotate_right_action)
        self.edit_menu.addAction(self.rotate_left_action)

        self.image_menu = self.menubar.addMenu('Изображение')
        self.image_menu.addSection('Фильтры')
        self.image_menu.addAction(self.black_white_action)

        self.help_menu = self.menubar.addMenu('Справка')
        self.help_menu.addAction(self.about_action)
