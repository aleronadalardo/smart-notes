from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QButtonGroup, QPushButton,
        QLabel, QListWidget, QLineEdit, QTextEdit,
        QInputDialog)
import json

notes = {
    "Welcome!" : {
        "text" : "This is the best note taking app in the world!", 
        "tags" : ["good", "instructions"]
    }
}

app = QApplication([])
window = QWidget()
window.setWindowTitle("Smart notes")

window.resize(900, 600)

#List of notes
label_notes = QLabel("List of notes")
list_note = QListWidget()
create_note = QPushButton("Create note")
delete_note = QPushButton("Delete note")
save_note = QPushButton("Save note")

#List of tags
label_tags = QLabel("List of tags")
list_tags = QListWidget()
add_tags = QPushButton("Add to note")
unpin_tags = QPushButton("Untag from note")
search_tags = QPushButton("Search notes by tag")

field_tag = QLineEdit("")
field_tag.setPlaceholderText("Enter tag...")
field_text = QTextEdit()

layout_notes = QHBoxLayout()
layout1 = QVBoxLayout()
layout2 = QVBoxLayout()

layout1.addWidget(field_text)
layout2.addWidget(label_notes)
layout2.addWidget(list_note)

row_1 = QHBoxLayout()
row_1.addWidget(create_note)
row_1.addWidget(delete_note)
row_2 = QVBoxLayout()
row_2.addWidget(save_note)
layout2.addLayout(row_1)
layout2.addLayout(row_2)

layout2.addWidget(label_tags)
layout2.addWidget(list_tags)
layout2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(add_tags)
row_3.addWidget(unpin_tags)
row_4 = QVBoxLayout()
row_4.addWidget(search_tags)
layout2.addLayout(row_3)
layout2.addLayout(row_4)

layout_notes.addLayout(layout1, stretch = 2)
layout_notes.addLayout(layout2, stretch = 1)
window.setLayout(layout_notes)

def add_note():
    note_name, ok = QInputDialog.getText(window, "Add note", "Note name:")
    if ok and note_name != "":
        notes[note_name] = {"text" : "", "tags" : []}
        list_note.addItem(note_name)
        list_tags.addItems(notes[note_name]["tags"])

def show_note():
    key = list_note.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["text"])
    list_tags.clear()
    list_tags.addItems(notes[key]["tags"])

def safe_note():
    if list_note.selectedItems():
        key = list_note.selectedItems()[0].text()
        notes[key]["text"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Note to save is not selected!")

def del_note():
    if list_note.selectedItems():
        key = list_note.selectedItems()[0].text()
        del notes[key]
        list_note.clear()
        list_tags.clear()
        field_text.clear()
        list_note.addItems(notes)
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Note to delete is not selected!")

def add_tag():
    if list_note.selectedItems():
        key = list_note.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["tags"]:
            notes[key]["tags"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Note to add a tag is not selected!")

def del_tag():
    if list_note.selectedItems():
        key = list_note.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["tags"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["tags"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Tag to delete is not selected!")

def search_tag():
    print(search_tags.text())
    tag = field_tag.text()
    if search_tags.text() == "Search notes by tag" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["tags"]:
                notes_filtered[note]=notes[note]
        search_tags.setText("Reset search")
        list_note.clear()
        list_tags.clear()
        list_note.addItems(notes_filtered)
        print(search_tags.text())
    elif search_tags.text() == "Reset search":
        field_tag.clear()
        list_note.clear()
        list_tags.clear()
        list_note.addItems(notes)
        search_tags.setText("Search notes by tag")
        print(search_tags.text())

create_note.clicked.connect(add_note)
save_note.clicked.connect(safe_note)
delete_note.clicked.connect(del_note)
list_note.itemClicked.connect(show_note)
add_tags.clicked.connect(add_tag)
unpin_tags.clicked.connect(del_tag)
search_tags.clicked.connect(search_tag)

with open("notes_data.json", "r") as file:
    notes = json.load(file)

list_note.addItems(notes)

window.show()
app.exec()