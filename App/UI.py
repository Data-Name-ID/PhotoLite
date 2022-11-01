import os

from typing import Type, Union, Tuple
from dataclasses import dataclass

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QMenu, QToolBar, QAction, QMenuBar

from .ImageArea import ImageArea
from .Config import PROGRAM_NAME


@dataclass()
class Menu:
    name: str
    text: str


@dataclass()
class Action:
    name: str
    text: str
    shortcut: str
    location: Union[Type[QToolBar], Type[QMenuBar]]
    menu_name: str
    menu_separator: str = ''
    separator: bool = False
    enabled: bool = False
    enabled_exception: bool = False


menu_list = (
    Menu('file', 'Файл'),
    Menu('edit', 'Редактирование'),
    Menu('image', 'Изображение'),
    Menu('view', 'Просмотр'),
    Menu('help', 'Помощь')
)

actions_list: Tuple[Action, ...] = (
    Action('open_file', 'Открыть...', 'Ctrl+O', QToolBar, 'file', 'Начало работы', enabled=True),
    Action('close_file', 'Закрыть', 'Ctrl+W', QMenuBar, 'file'),

    Action('save_file', 'Сохранить', 'Ctrl+S', QToolBar, 'file', 'Сохранение'),
    Action('save_as_file', 'Сохранить как...', 'Ctrl+Shift+S', QMenuBar, 'file'),

    Action('exit', 'Выход', 'Ctrl+Q', QMenuBar, 'file', 'Закрытие', enabled=True),

    Action('step_back', 'Шаг назад', 'Ctrl+Z', QToolBar, 'edit', 'Действия', separator=True, enabled_exception=True),
    Action('step_forward', 'Шаг вперёд', 'Ctrl+Y', QToolBar, 'edit', enabled_exception=True),

    Action('rotate_right', 'Повенуть на 90° по ч. с.', ']', QToolBar, 'edit', 'Трансформирование', separator=True),
    Action('rotate_left', 'Повенуть на 90° против ч. с.', '[', QToolBar, 'edit', ),

    Action('zoom_in', 'Приблизить', '=', QToolBar, 'view', 'Размер', True),
    Action('zoom_out', 'Отдалить', '-', QToolBar, 'view'),

    Action('black_white', 'Чёрно-белое', '', QMenuBar, 'image', 'Фильтры'),
    Action('inversion', 'Инверсия', '', QMenuBar, 'image'),

    Action('about', 'О программе', 'Ctrl+I', QMenuBar, 'help', 'Справка', enabled=True)
)



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
        self.image_area = ImageArea(main_window)
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
