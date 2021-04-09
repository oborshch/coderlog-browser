from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import os


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok
        self.buttonbox = QDialogButtonBox(QBtn)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("CoderLog Browser")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('data/images', 'logo.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Version 0.1"))
        layout.addWidget(QLabel("Copyright 2021 CoderLog"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)
        
        layout.addWidget(self.buttonbox)

        self.setLayout(layout)