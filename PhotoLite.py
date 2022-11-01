import sys
import sqlite3

from os import path, makedirs

from types import TracebackType
from typing import Optional, Type

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from App import *


class PhotoLite(QMainWindow, UI):  # type: ignore
    def __init__(self) -> None:
        super().__init__()
        self.init_ui(self)

        self._connect_actions()
        self._connect_db()

        self.show()

    def _connect_actions(self) -> None:
        self.open_file_action.triggered.connect(self._open_image_file)
        self.close_file_action.triggered.connect(self._close_image_file)

        self.save_file_action.triggered.connect(self.image_area.save_image)
        self.save_as_file_action.triggered.connect(lambda: self.image_area.save_image(True))

        self.exit_action.triggered.connect(self.close)

        self.step_forward_action.triggered.connect(lambda: self.image_area.to_history_step(1))
        self.step_back_action.triggered.connect(lambda: self.image_area.to_history_step(-1))

        self.rotate_left_action.triggered.connect(
            lambda: self.image_area.apply_filter(rotate_tool, 90)
        )
        self.rotate_right_action.triggered.connect(
            lambda: self.image_area.apply_filter(rotate_tool, -90)
        )

        self.zoom_in_action.triggered.connect(lambda: self._zoom_image(1.25))
        self.zoom_out_action.triggered.connect(lambda: self._zoom_image(0.8))

        self.black_white_action.triggered.connect(
            lambda: self.image_area.apply_filter(black_white_filter)
        )
        self.inversion_action.triggered.connect(
            lambda: self.image_area.apply_filter(inversion_filter)
        )

        self.about_action.triggered.connect(self._about_message)

    def _connect_db(self) -> None:
        if not path.exists('Data'):
            makedirs('Data')

        self.data_base = sqlite3.connect('Data/Main.db')
        self.db_cur = self.data_base.cursor()

        self.db_cur.execute('CREATE TABLE IF NOT EXISTS images(path TEXT PRIMARY KEY)')
        self.data_base.commit()

    def _open_image_file(self) -> None:
        if self._save_question():
            return None

        image_path = self.image_area.open_image_file()

        if image_path:
            self.db_cur.execute(f"INSERT OR IGNORE INTO images(path) VALUES('{image_path}')")
            self.data_base.commit()

            for action in actions_list:
                getattr(self, action.name + '_action').setEnabled(not action.enabled_exception)

    def _close_image_file(self) -> None:
        if self._save_question():
            return None

        self.image_area.close_image_file()

        for action in actions_list:
            getattr(self, action.name + '_action').setEnabled(action.enabled)

    def _zoom_image(self, ratio: float) -> None:
        zoom_value = self.image_area.resize_image(ratio)

        self.zoom_in_action.setEnabled(zoom_value < 3)
        self.zoom_out_action.setEnabled(zoom_value > 0.3)

    def _about_message(self) -> None:
        QMessageBox.about(self, f'О {PROGRAM_NAME}', ABOUT_DESCRIPTION)

    def _save_question(self) -> bool:
        if self.image_area.is_need_save():
            result = QMessageBox.warning(
                self, PROGRAM_NAME, 'Сохранить изменения?',
                QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel
            )

            if result == QMessageBox.Yes:
                self.image_area.save_image()

            if result == QMessageBox.Cancel:
                return True

        return False

    def closeEvent(self, event: QEvent) -> None:
        result = self._save_question()

        if result:
            event.ignore()
        else:
            self.data_base.close()


def _except_hook(cls: Type[BaseException], exception: BaseException,
                traceback: Optional[TracebackType]) -> None:
    sys.__excepthook__(cls, exception, traceback)


def main() -> None:
    application = QApplication(sys.argv)

    application.setAttribute(Qt.AA_UseHighDpiPixmaps)
    application.setStyle('Fusion')  # type: ignore

    window = PhotoLite()

    sys.excepthook = _except_hook
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
