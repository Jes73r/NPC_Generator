from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QComboBox,
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCompleter

import json
from pathlib import Path

def load_npc_types():
    data_path = Path(__file__).resolve().parents[2] / "data" / "npc_types.json"

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["npc_types"]



class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Generator")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        group = QGroupBox("NPC Optionen")
        group_layout = QVBoxLayout(group)

        # Lable NPC Typ
        type_label = QLabel("NPC Typ:")
        group_layout.addWidget(type_label)

        NPC_TYPES = load_npc_types()

        # ComboBox für NPC Typ
        self.type_combo = QComboBox()
        self.type_combo.setEditable(True)
        self.type_combo.setInsertPolicy(QComboBox.NoInsert) # Verhindert neue Einträge

        self.type_combo.addItem("")
        self.type_combo.addItems([t["name"] for t in NPC_TYPES])
        

        # Droppdown Laden
        self.type_combo.addItems(NPC_TYPES)
        
        # Autocomplete aktivieren
        completer = QCompleter([t["name"] for t in NPC_TYPES])
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.InlineCompletion)
        self.type_combo.setCompleter(completer)


        self.race_label = QLabel("Rasse:")
        self.race_combo = QComboBox()
        

        self.race_label.hide()
        self.race_combo.hide()

        def on_type_changed(text):
            self.race_combo.clear()

            for npc_type in NPC_TYPES:
                if npc_type["name"] == text and npc_type["races"]:
                    self.race_label.show()
                    self.race_combo.show()
                    self.race_combo.addItems(
                        [r["name"] for r in npc_type["races"]]
                    )
                    return

            # Kein passender Typ → Rassenfeld ausblenden
            self.race_label.hide()
            self.race_combo.hide()

        # --- Signal verbinden ---------------------------------------

        self.type_combo.currentTextChanged.connect(on_type_changed)

        # Layout hinzufügen
        group_layout.addWidget(self.type_combo) 
        layout.addWidget(group)
        group_layout.addWidget(self.race_label)
        group_layout.addWidget(self.race_combo)

        # Button zum Generieren
        generate_button = QPushButton("NPC generieren")
        layout.addWidget(generate_button)

        layout.addStretch()
