from typing import Any, Callable, List, Union

from PIL import Image, UnidentifiedImageError
from PIL.ImageQt import ImageQt

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QFileDialog, QMessageBox, QMainWindow

from .Config import *


class ImageArea(QLabel):
    def __init__(self, main_window: QMainWindow) -> None:
        super().__init__()

        self.main_window = main_window

        self.original_image: Image
        self.close_image_file()

        self.setScaledContents(True)
        self.setAlignment(Qt.AlignCenter)

    def open_image_file(self) -> Union[str, None]:
        image_path = QFileDialog.getOpenFileName(
            self, 'Открытие', '',
            f'Изображение ({"; ".join(image_formats)});; Все файлы (*.*)'
        )[0]

        if not image_path:
            return None

        try:
            self._set_image(image_path)
            self.image_path = image_path

            return image_path
        except UnidentifiedImageError:
            QMessageBox.warning(self, 'Ошибка', 'Указанный формат изображения не поддерживается!')

            return None

    def close_image_file(self) -> None:
        self.current_history_step = -1
        self.zoom_value = 1.0
        self.original_image = None
        self._set_is_saved(True)

        self.clear()

    def save_image(self, save_as: bool = False) -> None:
        if save_as:
            image_path = QFileDialog.getSaveFileName(
                self, 'Сохранение', '', ';;'.join(image_formats)
            )[0]

            if not image_path:
                return None
        else:
            image_path = self.image_path

        self.current_image.save(image_path)
        self._set_is_saved(True)

    def resize_image(self, ratio: float) -> float:
        self.zoom_value = round(self.zoom_value * ratio, 2)

        size = self.displayed_image.size()
        width, height = int(size.width() * self.zoom_value), int(size.height() * self.zoom_value)
        self.resize(QSize(width, height))

        return self.zoom_value

    def apply_filter(self, image_filter: Callable[..., Image.open], *args: Any) -> None:
        new_image = image_filter(self.current_image, *args)
        self._update_history(new_image)
        self._update_image(new_image)

        self._set_history_actions_enabled()

    def to_history_step(self, step: int) -> None:
        self.current_history_step += step

        history_image = self.history[self.current_history_step]
        self._update_image(history_image)

        self._set_history_actions_enabled()

    def is_need_save(self) -> bool:
        return self.original_image is not None and \
            (not self.is_saved[0] or self.current_history_step != self.is_saved[1])

    def _set_is_saved(self, is_saved: bool) -> None:
        self.is_saved = (is_saved, self.current_history_step)

    def _set_image(self, path: str) -> None:
        self.original_image = Image.open(path)
        self.current_image = self.original_image.copy()

        self.zoom_value = 1.0
        self.history: List[Image.open] = []
        self.current_history_step = -1

        self._update_image(self.current_image)
        self._update_history(self.current_image)
        self._set_is_saved(True)

    def _update_image(self, image: Image) -> None:
        self.current_image = image
        self._set_is_saved(False)

        self.displayed_image = ImageQt(self.current_image)
        self.setPixmap(QPixmap().fromImage(self.displayed_image))

        size = self.displayed_image.size()
        width, height = int(size.width() * self.zoom_value), int(size.height() * self.zoom_value)
        self.resize(QSize(width, height))

    def _update_history(self, image: Image) -> None:
        if len(self.history) - 1 != self.current_history_step:
            del self.history[self.current_history_step + 1:]

        if len(self.history) == SETTINGS['history_limit']:
            del self.history[0]
        else:
            self.current_history_step += 1

        self.history.append(image)

    def _set_history_actions_enabled(self) -> None:
        self.main_window.step_forward_action.setEnabled(len(self.history) > self.current_history_step + 1)
        self.main_window.step_back_action.setEnabled(self.current_history_step > 0)
