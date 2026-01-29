from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QGridLayout,
)
from PySide6.QtCore import Qt


class NpcPreview(QWidget):
    def __init__(self):
        super().__init__()

        NpcPreview.set_npc_data = set_npc_data
        NpcPreview._fill_grid = _fill_grid


        layout = QVBoxLayout(self)
        self.debug_label = QLabel("NPC Preview")
        layout.addWidget(self.debug_label)

        title = QLabel("NPC Vorschau")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        # --- Meta --------------------------------------------------
        self.meta_box = QGroupBox("Meta")
        self.meta_layout = QGridLayout(self.meta_box)
        layout.addWidget(self.meta_box)

         # --- Attribute ---------------------------------------------
        self.attr_box = QGroupBox("Attribute")
        self.attr_layout = QGridLayout(self.attr_box)
        layout.addWidget(self.attr_box)

        # --- Kampfwerte --------------------------------------------
        self.combat_box = QGroupBox("Kampfwerte")
        self.combat_layout = QGridLayout(self.combat_box)
        layout.addWidget(self.combat_box)

        # --- Talente -----------------------------------------------
        self.talent_box = QGroupBox("Talente")
        self.talent_layout = QGridLayout(self.talent_box)
        layout.addWidget(self.talent_box)

        layout.addStretch()
        
        self.set_npc_data({})

# -------------------------------------------------------------
# Öffentliche API: bekommt FERTIGE Daten
# -------------------------------------------------------------
def set_npc_data(self, npc_data: dict):

    self._fill_grid(self.meta_layout, npc_data.get("meta", {}))
    self._fill_grid(self.attr_layout, npc_data.get("base_attributes", {}))
    self._fill_grid(self.combat_layout, npc_data.get("combat_values", {}))
    self._fill_grid(self.talent_layout, npc_data.get("talents", {}))

# -------------------------------------------------------------
def _fill_grid(self, layout: QGridLayout, data: dict):
    # Layout leeren
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()

    for row, (key, value) in enumerate(data.items()):
        layout.addWidget(QLabel(str(key)), row, 0, Qt.AlignLeft)
        layout.addWidget(QLabel(str(value)), row, 1, Qt.AlignLeft)

