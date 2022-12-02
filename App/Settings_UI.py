"""
Описывает класс интерфейса окна настроек
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QPushButton,
)
from PyQt5.QtGui import QIcon


class Settings_UI(object):
    """
    Интерфейс окна настроек
    """

    def init_ui(self, window: QWidget) -> None:
        window.setWindowTitle('Настройки')
        window.setWindowIcon(QIcon('App/Icons/PhotoLite.svg'))
        window.setFixedSize(380, 80)

        self.main_layout = QVBoxLayout(window)
        self.history_layout = QHBoxLayout(window)

        self.histoty_label = QLabel(window)
        self.histoty_label.setText('Лимит истории')

        self.history_limit_value = QSpinBox(window)

        self.history_layout.addWidget(self.histoty_label)
        self.history_layout.addWidget(self.history_limit_value)

        self.buttons_layout = QHBoxLayout(window)

        self.save_button = QPushButton(window)
        self.save_button.setText('Сохранить')

        self.cancel_button = QPushButton(window)
        self.cancel_button.setText('Отмена')

        self.buttons_layout.addWidget(self.save_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(self.history_layout)
        self.main_layout.addLayout(self.buttons_layout)

        window.setLayout(self.main_layout)
