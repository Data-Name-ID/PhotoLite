from .Config import *

from typing import Any, Callable, List

from PIL import Image, UnidentifiedImageError
from PIL.ImageQt import ImageQt

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QFileDialog, QMessageBox


class ImageArea(QLabel):
    def __init__(self) -> None:
        super().__init__()

        self.zoom_value = 1.0
        self.history: List[Image.open] = []
        self.current_history_step = -1
        
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignCenter)

    def resize_image(self, ratio: float) -> float:
        self.zoom_value = round(self.zoom_value * ratio, 2)

        size = self.displayed_image.size()
        width, height = int(size.width() * self.zoom_value), int(size.height() * self.zoom_value)
        self.resize(QSize(width, height))

        return self.zoom_value

    def open_image_file(self) -> None:
        image_path = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            f'Изображение ({"; ".join(image_formats)});; Все файлы (*.*)'
        )[0]
        
        if not image_path:
            return None

        try:
            self._set_image(image_path)
        except UnidentifiedImageError:
            QMessageBox.warning(self, 'Ошибка', 'Указанный формат изображения не поддерживается!')

    def apply_filter(self, filter: Callable[..., Image.open], *args: Any) -> None:
        new_image = filter(self.current_image, *args)
        self._update_history(new_image)
        self._update_image(new_image)

    def to_history_step(self, n: int) -> None:
        """Перейти к предыдущему или последующему шагу

        Аргументы:
            n (int): int[-1] к предыдущему; int[1] к последующему
        """
        if (n < 0 and self.current_history_step > 0) or (n > 0 and len(self.history) > self.current_history_step + n):
            self.current_history_step += n

            history_image = self.history[self.current_history_step]
            self._update_image(history_image)

    def _set_image(self, path: str) -> None:
        self.original_image = Image.open(path)
        self.current_image = self.original_image.copy()
        
        self.zoom_value = 1
        self._update_history(self.current_image)
        self._update_image(self.current_image)

    def _update_image(self, image: Image) -> None:
        self.current_image = image

        self.displayed_image = ImageQt(self.current_image)
        self.setPixmap(QPixmap().fromImage(self.displayed_image))

        size = self.displayed_image.size()
        width, height = int(size.width() * self.zoom_value), int(size.height() * self.zoom_value)
        self.resize(QSize(width, height))

    def _update_history(self, image: Image) -> None:
        if len(self.history) - 1 != self.current_history_step:
            del self.history[-self.current_history_step + 1:]

        if len(self.history) == history_limit:
            del self.history[0]
        else:
            self.current_history_step += 1

        self.history.append(image)


if __name__ == '__main__':
    pass
