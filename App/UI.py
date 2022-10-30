import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QMenu, QToolBar, QAction

from .ImageArea import ImageArea
from .Config import menu_list, actions_list, PROGRAM_NAME


class UI(object):
    def init_ui(self, main_window: QMainWindow) -> None:
        main_window.setWindowTitle(PROGRAM_NAME)
        main_window.setWindowIcon(QIcon('App/Icons/PhotoLite.svg'))
        main_window.setMinimumSize(1000, 800)

        main_window.showMaximized()

        self._init_main_area(main_window)
        self._init_menubar(main_window)
        self._init_toolbar(main_window)
        self._init_actions(main_window)

    def _init_main_area(self, main_window: QMainWindow) -> None:
        self.image_area = ImageArea()
        self.scroll_area = QScrollArea(main_window)
        self.scroll_area.setAlignment(Qt.AlignCenter)

        self.scroll_area.setWidget(self.image_area)

        main_window.setCentralWidget(self.scroll_area)

    def _init_menubar(self, main_window: QMainWindow) -> None:
        self.menubar = main_window.menuBar()

        for menu in menu_list:
            setattr(self, f'{menu.name}_menu', self.menubar.addMenu(menu.text))

    def _init_toolbar(self, main_window: QMainWindow) -> None:
        self.toolbar = QToolBar('Инструменты')
        self.toolbar.setIconSize(QSize(26, 26))
        main_window.addToolBar(Qt.LeftToolBarArea, self.toolbar)

    def _init_actions(self, main_window: QMainWindow) -> None:
        for action in actions_list:
            menu: QMenu = getattr(self, f'{action.menu_name}_menu')

            if action.menu_separator:
                menu.addSection(action.menu_separator)

            if action.separator:
                self.toolbar.addSeparator()

            icon_path = f'App/Icons/Heroicons UI/{action.name}.svg'

            if os.path.isfile(icon_path):
                q_action = QAction(QIcon(icon_path), action.text, main_window)
            else:
                q_action = QAction(action.text, main_window)

            q_action.setShortcut(action.shortcut)
            q_action.setEnabled(action.enabled)

            if action.location is QToolBar:
                self.toolbar.addAction(q_action)

            menu.addAction(q_action)

            setattr(self, action.name + '_action', q_action)
