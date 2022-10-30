from typing import Type, Union, Tuple
from dataclasses import dataclass

from PyQt5.QtWidgets import QMenuBar, QToolBar


@dataclass()
class Action:
    name: str
    text: str
    shortcut: str
    location: Union[Type[QToolBar], Type[QMenuBar]]
    separator: bool = False
    enabled: bool = False


actions_list: Tuple[Action, ...] = (
    Action('open_file', 'Открыть...', 'Ctrl+O', QToolBar, enabled=True),
    Action('close_file', 'Закрыть', 'Ctrl+W', QMenuBar),
    Action('save_file', 'Сохранить', 'Ctrl+S', QToolBar, True),
    Action('save_as_file', 'Сохранить как...', 'Ctrl+Shift+S', QMenuBar),
    Action('exit', 'Выход', 'Ctrl+Q', QMenuBar, enabled=True),
    Action('step_back', 'Шаг назад', 'Ctrl+Z', QToolBar),
    Action('step_forward', 'Шаг вперёд', 'Ctrl+Y', QToolBar, True),
    Action('rotate_right', 'Повенуть на 90° по ч. с.', ']', QToolBar),
    Action('rotate_left', 'Повенуть на 90° против ч. с.', '[', QToolBar, True),
    Action('zoom_in', 'Приблизить', 'Ctrl+=', QToolBar),
    Action('zoom_out', 'Отдалить', 'Ctrl+-', QToolBar),
    Action('black_white', 'Чёрно-белое', '', QMenuBar),
    Action('about', 'О программе', 'Ctrl+I', QMenuBar, enabled=True)
)


program_name = 'PhotoLite'
about_description = """PhotoLite - небольшой фоторедактор, для применения различных эфектов к фото"""

image_formats = ('*.jpeg', '*.jpg', '*.png', '*.bmp')

history_limit = 15
