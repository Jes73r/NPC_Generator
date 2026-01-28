from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt


class NpcPreview(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("NPC Vorschau")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        preview_frame = QFrame()
        preview_frame.setFrameShape(QFrame.StyledPanel)
        preview_layout = QVBoxLayout(preview_frame)

        preview_layout.addWidget(QLabel("Name: <NPC Name>"))
        preview_layout.addWidget(QLabel("Typ: <NPC Typ>"))
        preview_layout.addWidget(QLabel("Region: <Region>"))
        preview_layout.addSpacing(10)
        preview_layout.addWidget(QLabel("Eigenschaften / Werte …"))
        preview_layout.addStretch()

        layout.addWidget(preview_frame)
