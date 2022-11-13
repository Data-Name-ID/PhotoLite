from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox
from PyQt5.QtGui import QIcon


class Settings_UI(object):
    def init_ui(self, window: QWidget) -> None:
        window.setWindowTitle('Настройки')
        window.setWindowIcon(QIcon('App/Icons/PhotoLite.svg'))
        window.setFixedSize(380, 60)

        self.main_layout = QVBoxLayout(window)
        self.history_layout = QHBoxLayout(window)

        self.histoty_label = QLabel(window)
        self.histoty_label.setText('Лимит истории')
        
        self.spinBox = QSpinBox(window)

        self.history_layout.addWidget(self.histoty_label)
        self.history_layout.addWidget(self.spinBox)

        self.main_layout.addLayout(self.history_layout)

        window.setLayout(self.main_layout)
