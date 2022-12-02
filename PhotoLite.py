"""
Главный файл приложения, точка входа. Описывает классы всех окон
"""

import sys
import sqlite3

from os import path, makedirs

from types import TracebackType
from typing import Optional, Type

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget

from App import *


class PhotoLite(QMainWindow, UI):  # type: ignore
    """
    Главное окно приложения
    """

    def __init__(self) -> None:
        super().__init__()
        self._connect_db()

        self.init_ui(self)

        self.settings_window = SettingsWindow(self)

        self._connect_actions()

        self.show()

    def _connect_actions(self) -> None:
        """
        Подключения Action'ов к кнопкам меню и ToolBar'а
        """
        self.open_file_action.triggered.connect(self._open_image_file)
        self.close_file_action.triggered.connect(self._close_image_file)

        self.save_file_action.triggered.connect(self.image_area.save_image)
        self.save_as_file_action.triggered.connect(
            lambda: self.image_area.save_image(True)
        )

        self.settings_action.triggered.connect(self._open_settings)

        self.exit_action.triggered.connect(self.close)

        self.step_forward_action.triggered.connect(
            lambda: self.image_area.to_history_step(1)
        )
        self.step_back_action.triggered.connect(
            lambda: self.image_area.to_history_step(-1)
        )

        self.rotate_left_action.triggered.connect(
            lambda: self.image_area.apply_filter(rotate_tool, 90)
        )
        self.rotate_right_action.triggered.connect(
            lambda: self.image_area.apply_filter(rotate_tool, -90)
        )
        self.flip_left_right_action.triggered.connect(
            lambda: self.image_area.apply_filter(flip_left_right_tool, -90)
        )
        self.flip_top_bottom_action.triggered.connect(
            lambda: self.image_area.apply_filter(flip_top_bottom_tool, -90)
        )

        self.zoom_in_action.triggered.connect(lambda: self._zoom_image(1.25))
        self.zoom_out_action.triggered.connect(lambda: self._zoom_image(0.8))

        self.black_white_action.triggered.connect(
            lambda: self.image_area.apply_filter(black_white_filter)
        )
        self.only_black_white_action.triggered.connect(
            lambda: self.image_area.apply_filter(only_black_white_filter)
        )
        self.inversion_action.triggered.connect(
            lambda: self.image_area.apply_filter(inversion_filter)
        )
        self.makeanagliph_action.triggered.connect(
            lambda: self.image_area.apply_filter(makeanagliph_filter)
        )
        self.blur_action.triggered.connect(
            lambda: self.image_area.apply_filter(blur_filter)
        )
        self.sharpen_action.triggered.connect(
            lambda: self.image_area.apply_filter(sharpen_filter)
        )
        self.smooth_action.triggered.connect(
            lambda: self.image_area.apply_filter(smooth_filter)
        )
        self.find_edges_action.triggered.connect(
            lambda: self.image_area.apply_filter(find_edges_filter)
        )
        self.emboss_action.triggered.connect(
            lambda: self.image_area.apply_filter(emboss_filter)
        )

        self.about_action.triggered.connect(self._about_message)

    def _connect_db(self) -> None:
        """
        Подключение базы данных или её создание, если её не существует
        """
        if not path.exists('Data'):
            makedirs('Data')

        self.data_base = sqlite3.connect('Data/Main.db')
        self.db_cur = self.data_base.cursor()

        self.db_cur.execute(
            'CREATE TABLE IF NOT EXISTS images(path TEXT PRIMARY KEY)'
        )
        self.db_cur.execute(
            'CREATE TABLE IF NOT EXISTS settings'
            + '(name TEXT PRIMARY KEY, value TEXT)'
        )

        for setting in SETTINGS:
            try:
                self.db_cur.execute(
                    f"SELECT * FROM settings where name = '{setting}'"
                )
                SETTINGS[setting] = int(
                    self.db_cur.execute(
                        f"SELECT value FROM settings WHERE name = '{setting}'"
                    ).fetchall()[0][0]
                )
            except:
                self.db_cur.execute(
                    f'INSERT INTO settings VALUES(?, ?)',
                    (setting, str(SETTINGS[setting])),
                )

    def _open_image_file(self) -> None:
        """
        Открытие файла изображения
        """
        if self._save_question():
            return None

        image_path = self.image_area.open_image_file()

        if image_path:
            self.db_cur.execute(
                f"INSERT OR IGNORE INTO images(path) VALUES('{image_path}')"
            )
            self.data_base.commit()

            for action in actions_list:
                getattr(self, action.name + '_action').setEnabled(
                    not action.enabled_exception
                )

    def _close_image_file(self) -> None:
        """
        Закрытие файла изображения
        """
        if self._save_question():
            return None

        self.image_area.close_image_file()

        for action in actions_list:
            getattr(self, action.name + '_action').setEnabled(action.enabled)

    def _zoom_image(self, ratio: float) -> None:
        """
        Зум изображения, либо приближение, либо отдаление
        """
        zoom_value = self.image_area.resize_image(ratio)

        self.zoom_in_action.setEnabled(zoom_value < 3)
        self.zoom_out_action.setEnabled(zoom_value > 0.3)

    def _about_message(self) -> None:
        """
        Открытие диалога 'О программе'
        """
        QMessageBox.about(self, f'О {PROGRAM_NAME}', ABOUT_DESCRIPTION)

    def _open_settings(self):
        """
        Открытие окна настроек
        """
        for setting in SETTINGS:
            getattr(self.settings_window, f'{setting}_value').setValue(
                int(
                    self.db_cur.execute(
                        f"SELECT value FROM settings WHERE name = '{setting}'"
                    ).fetchall()[0][0]
                )
            )

        self.settings_window.show()

    def _save_question(self) -> bool:
        """
        Открытие диалога сохранения изображения
        """
        if self.image_area.is_need_save():
            result = QMessageBox.warning(
                self,
                PROGRAM_NAME,
                'Сохранить изменения?',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            )

            if result == QMessageBox.Yes:
                self.image_area.save_image()

            if result == QMessageBox.Cancel:
                return True

        return False

    def closeEvent(self, event: QEvent) -> None:
        """
        Инициализация закрытия приложения
        """
        result = self._save_question()

        if result:
            event.ignore()
        else:
            self.data_base.commit()
            self.data_base.close()


class SettingsWindow(QWidget, Settings_UI):
    """
    Окно настроек приложения
    """

    def __init__(self, main_window: QMainWindow) -> QWidget:
        super().__init__()
        self.init_ui(self)

        self.main_window = main_window

        self.save_button.clicked.connect(self._save)
        self.cancel_button.clicked.connect(self._cancel)

    def _save(self) -> None:
        """
        Сохранение настроек
        """
        for setting in SETTINGS:
            self.main_window.db_cur.execute(
                f"UPDATE settings SET value = '"
                + getattr(self, f'{setting}_value').value()
                + "' WHERE name = '{setting}'"
            )

        self.close()

    def _cancel(self) -> None:
        """
        Закрытие окна настроек без сохранения
        """
        self.close()


def _except_hook(
    cls: Type[BaseException],
    exception: BaseException,
    traceback: Optional[TracebackType],
) -> None:
    """
    Включение вывода ошибок
    """
    sys.__excepthook__(cls, exception, traceback)


def main() -> None:
    """
    Точка входа в приложение
    """
    application = QApplication(sys.argv)

    application.setAttribute(Qt.AA_UseHighDpiPixmaps)
    application.setStyle('Fusion')  # type: ignore

    window = PhotoLite()

    sys.excepthook = _except_hook
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
