from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QComboBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QCompleter

import json
from pathlib import Path

class ControlPanel(QWidget):
    
    npc_data_changed = Signal(dict)
    
    def __init__(self):
        super().__init__()

        # --- NPC Typen laden ---------------------------------------
        npc_types_data = load_json_file("npc_types.json")["npc_types"]
        type_names = [t["name"] for t in npc_types_data]
        self.npc_types_by_id = {t["id"]: t for t in npc_types_data}

        print("Verfügbare NPC Typen:")
        for t in npc_types_data:
            print(f" - {t['name']} ({t['id']})")

        # --- Hauptlayout -------------------------------------------
        layout = QVBoxLayout(self)
        title = QLabel("Generator")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")

        layout.addWidget(title)
        
        # --- Layout der NPC Options Box-----------------------------------------------
        group = QGroupBox("NPC Optionen")
        group_layout = QVBoxLayout(group)
        type_label = QLabel("NPC Typ:")

        layout.addWidget(group)

        # --- Typ (Kategorie) ----------------------------------------
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

        group_layout.addWidget(type_label)
        group_layout.addWidget(self.type_combo) 

        # --- Rasse (Spezies) ----------------------------------------
        self.race_label = QLabel("Rasse:")
        self.race_combo = QComboBox()
        self.race_combo.setEditable(True)
        self.race_combo.setInsertPolicy(QComboBox.NoInsert) # Verhindert neue Einträge

        self.race_label.hide()
        self.race_combo.hide()

        group_layout.addWidget(self.race_label)
        group_layout.addWidget(self.race_combo)

        # --- Variante -----------------------------------------------
        self.variant_label = QLabel("Variante:")
        self.variant_combo = QComboBox()
        self.variant_combo.setEditable(True)
        self.variant_combo.setInsertPolicy(QComboBox.NoInsert)

        self.variant_label.hide()
        self.variant_combo.hide()

        group_layout.addWidget(self.variant_label)
        group_layout.addWidget(self.variant_combo)


        # --- Profile (Erfahrungsgrad) ------------------------------
        self.profile_label = QLabel("Erfahrungsgrad:")
        self.profile_combo = QComboBox()
        self.profile_combo.setEditable(True)
        self.profile_combo.setInsertPolicy(QComboBox.NoInsert) # Verhindert neue Einträge

        self.profile_label.hide()
        self.profile_combo.hide()   

        group_layout.addWidget(self.profile_label)
        group_layout.addWidget(self.profile_combo)        

        # --- Signal verbinden ---------------------------------------
        self.type_combo.currentIndexChanged.connect(lambda i: on_type_changed(self, i))
        self.race_combo.currentIndexChanged.connect(lambda i: on_race_changed(self, i))
        self.variant_combo.currentIndexChanged.connect(lambda i: on_variant_changed(self, i))
        self.race_combo.currentIndexChanged.connect(lambda i: on_profile_changed(self, i))
        
        self.type_combo.currentIndexChanged.connect(lambda _: emit_npc_data(self))
        self.race_combo.currentIndexChanged.connect(lambda _: emit_npc_data(self))
        self.variant_combo.currentIndexChanged.connect(lambda _: emit_npc_data(self))
        self.profile_combo.currentIndexChanged.connect(lambda _: emit_npc_data(self))

        # Button zum Generieren
        generate_button = QPushButton("NPC generieren")
        layout.addWidget(generate_button)

        layout.addStretch()

# --- Funktionen ---------------------------------------------#

def on_type_changed(panel, _):
    reset_all_submenus(panel)
    
    npc_type_id = panel.type_combo.currentData()
    if not npc_type_id:
        return

    if npc_type_id == "kulturschaffend":
        handle_kulturschaffende(panel)

    elif npc_type_id == "tier":
        handle_tiere(panel)    
    
def handle_kulturschaffende(panel):
    panel.race_combo.clear()
    
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

def handle_tiere(panel):
    panel.race_combo.clear()

    animals = load_json_folder("tiere")
    if not animals:
        panel.race_label.hide()
        panel.race_combo.hide()
        return
    
    panel.race_label.setText("Tierart")
    panel.race_label.show()
    panel.race_combo.show()

    panel.race_combo.addItem("", None)

    for animal_list in animals:
        for animal in animal_list:
            panel.race_combo.addItem(animal["name"], animal["id"])

def on_race_changed(panel, _):
    panel.variant_combo.clear()

    species_id = panel.race_combo.currentData()
    if not species_id:
        panel.variant_label.hide()
        panel.variant_combo.hide()
        return

    # Spezies-Datei laden (z. B. achaz.json)
    species_file = f"kulturschaffende/{species_id}.json"
    species_data = load_json_file(species_file)

    variants = species_data.get("variants", [])
    if not variants:
        panel.variant_label.hide()
        panel.variant_combo.hide()
        return

    panel.variant_label.show()
    panel.variant_combo.show()
    panel.variant_combo.addItem("", None)

    for variant in variants:
        panel.variant_combo.addItem(variant["name"], variant["id"])

    # Profil-Auswahl zurücksetzen (wichtig!)
    panel.profile_label.hide()
    panel.profile_combo.hide()
    panel.profile_combo.clear()

def on_variant_changed(panel, _):
    panel.profile_combo.clear()

    species_id = panel.race_combo.currentData()
    variant_id = panel.variant_combo.currentData()

    if not species_id or not variant_id:
        panel.profile_label.hide()
        panel.profile_combo.hide()
        return

    # Spezies-Datei laden (z. B. achaz.json)
    species_file = f"kulturschaffende/{species_id}.json"
    species_data = load_json_file(species_file)

    variants = species_data.get("variants", [])
    variant = next((v for v in variants if v["id"] == variant_id), None)

    if not variant:
        panel.profile_label.hide()
        panel.profile_combo.hide()
        return

    profiles = variant.get("profiles", [])

    # Nur ein Profil → kein Dropdown anzeigen
    if len(profiles) <= 1:
        panel.profile_label.hide()
        panel.profile_combo.hide()
        return

    # Mehrere Profile → Dropdown anzeigen
    panel.profile_label.show()
    panel.profile_combo.show()
    panel.profile_combo.addItem("", None)

    for profile in profiles:
        panel.profile_combo.addItem(profile["name"], profile["id"])

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

    npc_data = build_npc_data(panel)
    panel.npc_data_changed.emit(npc_data)

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

def build_npc_data(panel) -> dict:
    species_id = panel.race_combo.currentData()
    variant_id = panel.variant_combo.currentData()
    profile_id = panel.profile_combo.currentData()

    if not species_id or not variant_id:
        return {}

    # --- Spezies laden -------------------------------------------
    species_file = f"kulturschaffende/{species_id}.json"
    species_data = load_json_file(species_file)

    # --- Variante finden -----------------------------------------
    variant = next(
        (v for v in species_data["variants"] if v["id"] == variant_id),
        None
    )
    if not variant:
        return {}

    # --- Basisdaten ----------------------------------------------
    npc_data = {
        "meta": species_data.get("meta", {}),
        "base_attributes": {},
        "combat_values": {},
        "talents": {},
    }

    # --- Profil auswählen ----------------------------------------
    resolved_profile = resolve_variant(species_data, variant_id, profile_id)

    npc_data["base_attributes"] = resolved_profile.get("base_attributes", {})
    npc_data["combat_values"] = resolved_profile.get("combat_values", {})
    npc_data["talents"] = resolved_profile.get("talents", {})
    npc_data["special_abilities"] = resolved_profile.get("special_abilities", [])
    npc_data["advantages"] = resolved_profile.get("advantages", [])
    npc_data["disadvantages"] = resolved_profile.get("disadvantages", [])


    return npc_data

def emit_npc_data(panel):
    npc_data = build_npc_data(panel)
    if npc_data:
        panel.npc_data_changed.emit(npc_data)

def deep_merge(base: dict, override: dict) -> dict:
    result = dict(base)

    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result

def resolve_profile(variant: dict, profile_id: str) -> dict:
    profiles = {p["id"]: p for p in variant.get("profiles", [])}
    profile = profiles.get(profile_id)

    if not profile:
        return {}

    # --- Basisprofil bestimmen -----------------------------------
    if "inherits" in profile:
        base_profile = resolve_profile(variant, profile["inherits"])
    else:
        base_profile = profile

    # --- Modifier anwenden ---------------------------------------
    modifiers = profile.get("modifiers", {})
    resolved = deep_merge(base_profile, modifiers)

    # --- Zusätzliche Sonderfertigkeiten ---------------------------
    if "special_abilities_add" in profile:
        resolved.setdefault("special_abilities", [])
        resolved["special_abilities"] += profile["special_abilities_add"]

    return resolved

def resolve_variant(species_data: dict, variant_id: str, profile_id: str | None) -> dict:
    variants = {v["id"]: v for v in species_data.get("variants", [])}
    variant = variants.get(variant_id)

    if not variant:
        return {}

    # --- Inheritance ---------------------------------------------
    if "inherits" in variant:
        base_variant_id = variant["inherits"].get("variant")
        base_profile_id = variant["inherits"].get("profile")

        base_variant = variants.get(base_variant_id)
        if not base_variant:
            return {}

        resolved_profile = resolve_profile(base_variant, base_profile_id)
        resolved = dict(resolved_profile)

        # Variant-Modifier anwenden
        modifiers = variant.get("modifiers", {})
        resolved = deep_merge(resolved, modifiers)

        # Zusätzliche Sonderfertigkeiten
        if "special_abilities_add" in variant:
            resolved.setdefault("special_abilities", [])
            resolved["special_abilities"] += variant["special_abilities_add"]

        # Verhalten überschreiben
        if "behavior_override" in variant:
            resolved["behavior"] = variant["behavior_override"]

        return resolved

    # --- Keine Inheritance → normale Variante --------------------
    profiles = variant.get("profiles", [])
    resolved_profile = resolve_profile(variant, profile_id)
    return resolved_profile

def reset_all_submenus(panel):
    panel.race_label.hide()
    panel.race_combo.hide()
    panel.variant_label.hide()
    panel.variant_combo.hide()
    panel.profile_label.hide()
    panel.profile_combo.hide()

#def _emit_test_data(panel, _):
#       panel.npc_data_changed.emit({
#           "meta": {
#               "Rasse": "Achaz",
#               "Variante": "Achaz-Krieger"
#           },
#           "base_attributes": {
#               "MU": 12,
#               "KL": 12,
#               "IN": 14
#           },
#           "combat_values": {
#               "LeP": 33,
#               "INI": "13+1W6"
#           },
#           "talents": {
#               "Schwimmen": 8,
#               "Sinnesschärfe": 6
#           }
#           })