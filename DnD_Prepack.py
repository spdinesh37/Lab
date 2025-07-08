import csv
import os
import sys
import time
from os import listdir, mkdir, path, system, getenv
from platform import system
from re import match
from shutil import copy2, rmtree

from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QFont
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton, QVBoxLayout,
                               QFileDialog, QHBoxLayout, QMessageBox, QProgressDialog)

class FormData:
    def __init__(self, output_folder, processing_folder, responsible_org, collection_name, item_type, feature_x,
                 feature_y, blazer_id):
        self.output_folder = output_folder
        self.processing_folder = processing_folder
        self.responsible_org = responsible_org
        self.collection_name = collection_name
        self.item_type = item_type
        self.feature_x = feature_x
        self.feature_y = feature_y
        self.blazer_id = blazer_id


# Custom QLineEdit to handle mouse press
class ClickableLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "")
        if folder_path:
            self.setText(folder_path)


class SimpleForm(QWidget):
    def __init__(self):
        super().__init__()
        self.form_data = None
        self.setWindowTitle("DnD Pre-Packer")
        self.setFixedSize(646, 504)

        self.title_label = QLabel('DnD\nPre-Packer')
        self.title_label.setAlignment(Qt.AlignCenter)

        self.title_label.setFixedSize(560, 60)
        self.title_label.setFont(QFont('Garamond', 15, QFont.Bold, italic=True))

        gray = '#D3D3D3'  # Replace with your actual color value
        self.title_label.setStyleSheet(f"""
            color: black;
            background-color: {gray};
            border: 1px inset gray;  /* SUNKEN effect */
        """)

        # --- Widgets ---
        self.label = QLabel("Output Folder :")
        self.output_folder = ClickableLineEdit()
        self.output_folder.setPlaceholderText("Click to browse folder...")
        self.output_folder.setReadOnly(True)

        # --- Widgets ---
        self.label2 = QLabel('Processing Folder :')
        self.processing_folder = ClickableLineEdit()
        self.processing_folder.setPlaceholderText("Click to browse folder...")
        self.processing_folder.setReadOnly(True)

        self.label3 = QLabel('Responsible Org:')
        self.responsible_org = QComboBox()
        self.responsible_org.addItems(["Department of Art and Art HIstory", "Option A2", "Option A3"])

        self.label4 = QLabel('Collection Name:')
        self.collection_name = QComboBox()
        self.collection_name.addItems(["Birmingham Architecture", "Option B2", "Option B3"])

        self.label5 = QLabel('ItemType:')
        self.item_type = QComboBox()
        self.item_type.addItems(["digitized slide", "Option C2", "Option C3"])

        self.bLable = QLabel("Blazer ID:")
        self.bLable.setFont(QFont('Calibri', 11, QFont.Bold))
        # Blazer ID input (alphanumeric only)
        self.blazer_id = QLineEdit()
        self.blazer_id.setPlaceholderText("e.g., ab1234")
        regex = QRegularExpression("^[a-zA-Z0-9]+$")
        validator = QRegularExpressionValidator(regex)
        self.blazer_id.setValidator(validator)

        self.feature_x = QCheckBox("Collate Objects")
        self.checkbox2 = QCheckBox("Generate CSV Loader")

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(QApplication.instance().quit)

        self.progress_dialog = None

        self.label.setFont(QFont('Calibre', 11, QFont.Bold))
        self.label2.setFont(QFont('Calibre', 11, QFont.Bold))
        self.label3.setFont(QFont('Calibre', 11, QFont.Bold))
        self.label4.setFont(QFont('Calibre', 11, QFont.Bold))
        self.label5.setFont(QFont('Calibre', 11, QFont.Bold))


        # --- Layout ---
        layout = QVBoxLayout()

        layout.addWidget(self.title_label, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Create a horizontal layout
        row_layout1 = QHBoxLayout()
        row_layout1.addWidget(self.label)
        row_layout1.addWidget(self.output_folder)
        layout.addLayout(row_layout1)

        row_layout2 = QHBoxLayout()
        row_layout2.addWidget(self.label2)
        row_layout2.addWidget(self.processing_folder)
        layout.addLayout(row_layout2)

        row_layout3 = QHBoxLayout()
        row_layout3.addWidget(self.label3)
        row_layout3.addWidget(self.responsible_org)
        layout.addLayout(row_layout3)

        row_layout4 = QHBoxLayout()
        row_layout4.addWidget(self.label4)
        row_layout4.addWidget(self.collection_name)
        layout.addLayout(row_layout4)

        row_layout5 = QHBoxLayout()
        row_layout5.addWidget(self.label5)
        row_layout5.addWidget(self.item_type)
        layout.addLayout(row_layout5)

        row_layout = QHBoxLayout()
        row_layout.addWidget(self.bLable)

        row_layout.addWidget(self.blazer_id)
        # Add the horizontal layout to the vertical layout
        layout.addLayout(row_layout)

        row_layout6 = QHBoxLayout()
        row_layout6.addWidget(self.feature_x)
        row_layout6.addWidget(self.checkbox2)
        layout.addLayout(row_layout6)

        self.setLayout(layout)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.quit_button)

        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(0)
        for row in [row_layout1, row_layout2, row_layout3, row_layout4, row_layout5, row_layout6, row_layout]:
            row.setSpacing(5)
            row.setContentsMargins(10, 15, 10, 10)

    def submit(self):
        self.form_data = FormData(output_folder=self.output_folder.text(),
            processing_folder=self.processing_folder.text(), responsible_org=self.responsible_org.currentText(),
            collection_name=self.collection_name.currentText(), item_type=self.item_type.currentText(),
            feature_x=self.feature_x.isChecked(), feature_y=self.checkbox2.isChecked(), blazer_id=self.blazer_id.text())
        self.l = [self.output_folder.text(), self.processing_folder.text(), self.responsible_org.currentText(),
            self.collection_name.currentText(), self.item_type.currentText(), self.blazer_id.text(),
            self.feature_x.isChecked(), self.checkbox2.isChecked(), ]

        self.run_procs()

    def handle_form_data(self, data: FormData):
        print("Output Folder:", data.output_folder)
        print("Processing Folder:", data.processing_folder)
        print("Responsible Org:", data.responsible_org)
        print("Collection Name:", data.collection_name)
        print("Item Type:", data.item_type)
        print("Feature X:", data.feature_x)
        print("Feature Y:", data.feature_y)
        print("Blazer ID:", data.blazer_id)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleForm()
    window.show()
    sys.exit(app.exec())
