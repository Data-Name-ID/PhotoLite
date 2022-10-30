from typing import Type, Union, Tuple
from dataclasses import dataclass

from PyQt5.QtWidgets import QMenuBar, QToolBar


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

    Action('step_back', 'Шаг назад', 'Ctrl+Z', QToolBar, 'edit', 'Действия', separator=True),
    Action('step_forward', 'Шаг вперёд', 'Ctrl+Y', QToolBar, 'edit'),

    Action('rotate_right', 'Повенуть на 90° по ч. с.', ']', QToolBar, 'edit', 'Трансформирование', separator=True),
    Action('rotate_left', 'Повенуть на 90° против ч. с.', '[', QToolBar, 'edit', ),

    Action('zoom_in', 'Приблизить', 'Ctrl+=', QToolBar, 'view', 'Размер', True),
    Action('zoom_out', 'Отдалить', 'Ctrl+-', QToolBar, 'view'),

    Action('black_white', 'Чёрно-белое', '', QMenuBar, 'image', 'Фильтры'),

    Action('about', 'О программе', 'Ctrl+I', QMenuBar, 'help', 'Справка', enabled=True)
)

PROGRAM_NAME = 'PhotoLite'
ABOUT_DESCRIPTION = """PhotoLite - небольшой фоторедактор, для применения различных эфектов к фото"""

image_formats = ('*.jpeg', '*.jpg', '*.png', '*.bmp')

HISTORY_LIMIT = 15
