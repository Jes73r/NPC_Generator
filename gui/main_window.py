from PySide6.QtWidgets import QMainWindow, QSplitter
from PySide6.QtCore import Qt

from gui.widgets.control_panel import ControlPanel
from gui.widgets.npc_preview import NpcPreview


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DSA NPC Generator")
        self.resize(1200, 800)

        splitter = QSplitter(Qt.Horizontal)

        self.control_panel = ControlPanel()
        self.npc_preview = NpcPreview()

        splitter.addWidget(self.control_panel)
        splitter.addWidget(self.npc_preview)

        # Verhältnis links / rechts (wichtig für Vorschau!)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        self.setCentralWidget(splitter)
        
        self.control_panel.npc_data_changed.connect(self.npc_preview.set_npc_data)

