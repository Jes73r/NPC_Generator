from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QGridLayout,
    QSpinBox,
)
from PySide6.QtCore import Qt
import re

class NpcPreview(QWidget):
    def __init__(self):
        super().__init__()
        self.attribute_spins = {} 
        NpcPreview.set_npc_data = set_npc_data
        NpcPreview._fill_grid = _fill_grid
        NpcPreview._fill_attributes = _fill_attributes
        NpcPreview.fill_charackter_sheet = fill_charackter_sheet

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
    self.fill_charackter_sheet(self.attr_layout, npc_data.get("base_attributes", {}), npc_data.get("combat_values", {}))

    #self._fill_attributes(self.attr_layout, npc_data.get("base_attributes", {}))
#
    #self._fill_grid(self.combat_layout, npc_data.get("combat_values", {}))
    #self._fill_grid(self.talent_layout, npc_data.get("talents", {}))
# -------------------------------------------------------------
def fill_charackter_sheet(self, layout, attributes: dict, combat_values: dict):
    ATTRIBUTE_ORDER = ["MU", "KL", "IN", "CH", "FF", "GE", "KO", "KK"] 
    COMBAT_ORDER = ["LeP", "INI", "AT_waffenlos", "PA_waffenlos", "FK_wurfspeer", "RS", "BE"]    
    
    # Layout leeren
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()    

    # Kopfzeile Attribute
    for col, key in enumerate(ATTRIBUTE_ORDER):
        layout.addWidget(QLabel(key), 0, col, Qt.AlignCenter)

    # Werte Attribute
    for col, key in enumerate(ATTRIBUTE_ORDER):
        if key not in attributes:
            continue
        spin = QSpinBox()
        spin.setStyleSheet("""
            QSpinBox {
                min-height: 32px;
                min-width: 100px;
                font-size: 14px;
            }
            """)
        spin.setRange(1, 30)
        spin.setValue(attributes[key])
        layout.addWidget(spin, 1, col, Qt.AlignCenter)  

    # Abstand
    base_row = 2

    # Kopfzeile Kampf
    for col, key in enumerate(COMBAT_ORDER):
        layout.addWidget(QLabel(key), base_row, col, Qt.AlignCenter)

    # Werte Kampf
    for col, key in enumerate(COMBAT_ORDER):
        if key not in combat_values:
            continue

        # Sonderfall INI
        if key == "INI":
            raw = combat_values[key]
            base_ini = parse_ini(raw)

            spin = QSpinBox()
            spin.setRange(1, 30)
            spin.setValue(base_ini)
            spin.setAlignment(Qt.AlignCenter)

            spin.setStyleSheet("""
                QSpinBox {
                    min-height: 32px;
                    min-width: 100px;
                    font-size: 14px;
                }
            """)

            layout.addWidget(spin, base_row + 1, col)
            layout.addWidget(QLabel("+ 1W6"), base_row + 2, col, Qt.AlignCenter)
            continue  

        # Normalfall
        value = combat_values.get(key, 0)
        try:
            value = int(value)
        except (TypeError, ValueError):
            value = 0

        spin = QSpinBox()
        spin.setRange(0, 50)
        spin.setValue(value)
        spin.setAlignment(Qt.AlignCenter)

        spin.setStyleSheet("""
            QSpinBox {
                min-height: 32px;
                min-width: 100px;
                font-size: 14px;
            }
        """)

        layout.addWidget(spin, base_row + 1, col)


def parse_ini(value: str) -> int:
    match = re.match(r"(\d+)", value)
    return int(match.group(1)) if match else 0


def _fill_attributes(self, layout: QGridLayout, attributes: dict):
    # Layout leeren
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
    
    order = ["MU", "KL", "IN", "CH", "FF", "GE", "KO", "KK"] 
    print(attributes)
    col = 0
    for key in order:
        if key not in attributes:
            continue

        label = QLabel(key)
        spin = QSpinBox()

        spin.setStyleSheet("""
            QSpinBox {
                min-height: 32px;
                min-width: 100px;
                font-size: 14px;
            }
            """)

        spin.setRange(1, 30)
        spin.setValue(attributes[key])
        
        if key not in combat_values:
            continue
        spin.setValue(combat_values[key])


        layout.addWidget(label, 0, col, Qt.AlignCenter)
        layout.addWidget(spin, 1, col, Qt.AlignCenter)
        col += 1


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

