import sys

from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox,
    QCheckBox, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout
)
from PySide6.QtCore import Qt, QRegularExpression


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
        self.setWindowTitle("PySide6 GUI Example")
        self.setFixedSize(300, 400)

        # --- Widgets ---
        self.label = QLabel("Select a folder:")
        self.text_input = ClickableLineEdit()
        self.text_input.setPlaceholderText("Click to browse folder...")
        self.text_input.setReadOnly(True)

        # --- Widgets ---
        self.label2 = QLabel("Select a folder2:")
        self.text_input2 = ClickableLineEdit()
        self.text_input2.setPlaceholderText("Click to browse folder...")
        self.text_input2.setReadOnly(True)


        self.dropdown1 = QComboBox()
        self.dropdown1.addItems(["Option A1", "Option A2", "Option A3"])

        self.dropdown2 = QComboBox()
        self.dropdown2.addItems(["Option B1", "Option B2", "Option B3"])

        self.dropdown3 = QComboBox()
        self.dropdown3.addItems(["Option C1", "Option C2", "Option C3"])

        # Blazer ID input (alphanumeric only)
        self.label_blazer = QLabel("Enter Blazer ID:")
        self.blazer_input = QLineEdit()
        self.blazer_input.setPlaceholderText("e.g., ab1234")
        regex = QRegularExpression("^[a-zA-Z0-9]+$")
        validator = QRegularExpressionValidator(regex)
        self.blazer_input.setValidator(validator)

        self.checkbox1 = QCheckBox("Enable feature X")
        self.checkbox2 = QCheckBox("Enable feature Y")

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(QApplication.instance().quit)

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.label2)
        layout.addWidget(self.text_input2)
        layout.addWidget(self.dropdown1)
        layout.addWidget(self.dropdown2)
        layout.addWidget(self.dropdown3)
        layout.addWidget(self.label_blazer)
        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)
        layout.addWidget(self.quit_button)
        # Create a horizontal layout
        row_layout = QHBoxLayout()
        row_layout.addWidget(QLabel("Blazer ID:"))
        row_layout.addWidget(self.blazer_input)

        # Add the horizontal layout to the vertical layout
        layout.addLayout(row_layout)
        self.setLayout(layout)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleForm()
    window.show()
    sys.exit(app.exec())
