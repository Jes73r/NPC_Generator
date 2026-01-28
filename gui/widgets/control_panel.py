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

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        npc_types_data = load_json_file("npc_types.json")["npc_types"]
        type_names = [t["name"] for t in npc_types_data]
        self.npc_types_by_id = {t["id"]: t for t in npc_types_data}

        layout = QVBoxLayout(self)

        title = QLabel("Generator")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        group = QGroupBox("NPC Optionen")
        group_layout = QVBoxLayout(group)

        # Lable NPC Typ
        type_label = QLabel("NPC Typ:")
        group_layout.addWidget(type_label)


        # ComboBox für NPC Typ
        self.type_combo = QComboBox()
        self.type_combo.setEditable(True)
        self.type_combo.setInsertPolicy(QComboBox.NoInsert) # Verhindert neue Einträge       

        self.type_combo.addItem("", None)  # Leerer Eintrag
        for t in npc_types_data:
            self.type_combo.addItem(t["name"], t["id"])
        
        # Autocomplete (NUR strings!)
        line_edit = self.type_combo.lineEdit()
        
        # Autocomplete aktivieren
        completer = QCompleter(type_names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.InlineCompletion)
        line_edit.setCompleter(completer)
        self.type_combo.setCompleter(completer)


        self.race_label = QLabel("Rasse:")
        self.race_combo = QComboBox()
        self.race_combo.setEditable(True)
        self.race_combo.setInsertPolicy(QComboBox.NoInsert) # Verhindert neue Einträge

        self.race_label.hide()
        self.race_combo.hide()

        # --- Profile (Erfahrungsgrad) ------------------------------
        self.profile_label = QLabel("Erfahrungsgrad:")
        self.profile_combo = QComboBox()
        self.profile_combo.setEditable(True)
        self.profile_combo.setInsertPolicy(QComboBox.NoInsert) # Verhindert neue Einträge

        self.profile_label.hide()
        self.profile_combo.hide()           

        # --- Signal verbinden ---------------------------------------
        self.type_combo.currentIndexChanged.connect(lambda i: on_type_changed(self, i))
        self.race_combo.currentIndexChanged.connect(lambda i: on_profile_changed(self, i))

        # Layout hinzufügen
        group_layout.addWidget(self.type_combo) 
        layout.addWidget(group)

        group_layout.addWidget(self.race_label)
        group_layout.addWidget(self.race_combo)

        group_layout.addWidget(self.profile_label)
        group_layout.addWidget(self.profile_combo)

        # Button zum Generieren
        generate_button = QPushButton("NPC generieren")
        layout.addWidget(generate_button)

        layout.addStretch()

# --- Funktionen ---------------------------------------------#

def on_type_changed(panel, _):
    panel.race_combo.clear()

    npc_type_id = panel.type_combo.currentData()
    if not npc_type_id:
        panel.race_label.hide()
        panel.race_combo.hide()
        return

    npc_type = panel.npc_types_by_id.get(npc_type_id)
    if not npc_type:
        return

    species_data = load_json_folder("kulturschaffende")
    if not species_data:
        panel.race_label.hide()
        panel.race_combo.hide()
        return
    
    panel.race_label.show()
    panel.race_combo.show()
    panel.race_combo.addItem("",None)
    for species in species_data:
        panel.race_combo.addItem(species["name"], species["id"])


    line_edit = panel.race_combo.lineEdit()
    
    species_names = [s["name"] for s in species_data]
    # Autocomplete aktivieren
    completer = QCompleter(species_names)
    completer.setCaseSensitivity(Qt.CaseInsensitive)
    completer.setCompletionMode(QCompleter.InlineCompletion)
    line_edit.setCompleter(completer)
    panel.race_combo.setCompleter(completer)

def on_profile_changed(panel, _):
    species_id = panel.race_combo.currentData()
    
    if not species_id:
        panel.profile_label.hide()
        panel.profile_combo.hide()
        return
    # Spezies-Datei laden (z. B. achaz.json)
    species_file = f"kulturschaffende/{species_id}.json"
    species_data = load_json_file(species_file)
    profiles = species_data.get("profiles", [])
    if not profiles:
        panel.profile_label.hide()
        panel.profile_combo.hide()
        return
    
    panel.profile_label.show()
    panel.profile_combo.show()
    panel.profile_combo.clear()
    panel.profile_combo.addItem("", None)
    for profile in profiles:
        panel.profile_combo.addItem(profile["name"], profile["id"])
    
    line_edit = panel.profile_combo.lineEdit()
    profile_names = [p["name"] for p in profiles]
    # Autocomplete aktivieren
    completer = QCompleter(profile_names)
    completer.setCaseSensitivity(Qt.CaseInsensitive)
    completer.setCompletionMode(QCompleter.InlineCompletion)
    line_edit.setCompleter(completer)
    panel.profile_combo.setCompleter(completer)

def load_json_file(filename: str):
    base_path = Path(__file__).resolve().parents[2]
    data_path = base_path / "data" / filename

    if not data_path.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_json_folder(folder_name: str):
    base_path = Path(__file__).resolve().parents[2]
    folder_path = base_path / "data" / folder_name

    if not folder_path.exists() or not folder_path.is_dir():
        raise FileNotFoundError(f"Ordner nicht gefunden: {folder_path}")

    data = []

    for file_path in folder_path.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data.append(json.load(f))

    return data