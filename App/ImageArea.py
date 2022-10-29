from .Config import *

from typing import Any, Callable, List, Tuple

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
        self._update_image(new_image)

    def _set_image(self, path: str) -> None:
        self.original_image = Image.open(path)
        self.current_image = self.original_image.copy()
        
        self.zoom_value = 1
        self._update_image(self.current_image)

    def _update_image(self, image: Image) -> None:
        self._update_history(image)
        self.current_image = image

        self.displayed_image = ImageQt(self.current_image)
        self.setPixmap(QPixmap().fromImage(self.displayed_image))

        size = self.displayed_image.size()
        width, height = int(size.width() * self.zoom_value), int(size.height() * self.zoom_value)
        self.resize(QSize(width, height))

    def _update_history(self, image: Image) -> None:
        self.history.append(image)


if __name__ == '__main__':
    pass
