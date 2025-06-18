import sys

from PySide6.QtGui import QRegularExpressionValidator, QFont
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
        self.setWindowTitle("DnD Pre-Packer")
        self.setFixedSize(646, 504)

        self.title_label = QLabel('DnD\nPre-Packer')
        self.title_label.setAlignment(Qt.AlignCenter)

        self.title_label.setFixedSize(560,60)
        self.title_label.setFont(QFont('Garamond', 15, QFont.Bold, italic = True))

        gray = '#D3D3D3'  # Replace with your actual color value
        self.title_label.setStyleSheet(f"""
            color: black;
            background-color: {gray};
            border: 1px inset gray;  /* SUNKEN effect */
        """)






        # --- Widgets ---
        self.label = QLabel("Output Folder :")
        self.text_input = ClickableLineEdit()
        self.text_input.setPlaceholderText("Click to browse folder...")
        self.text_input.setReadOnly(True)

        # --- Widgets ---
        self.label2 = QLabel('Processing Folder :')
        self.text_input2 = ClickableLineEdit()
        self.text_input2.setPlaceholderText("Click to browse folder...")
        self.text_input2.setReadOnly(True)

        self.label3 = QLabel('Responsible Org:')
        self.dropdown1 = QComboBox()
        self.dropdown1.addItems(["Department of Art and Art HIstory", "Option A2", "Option A3"])

        self.label4 = QLabel('Collection\nName:')
        self.dropdown2 = QComboBox()
        self.dropdown2.addItems(["Birmingham Architecture", "Option B2", "Option B3"])

        self.label5 = QLabel('ItemType:')
        self.dropdown3 = QComboBox()
        self.dropdown3.addItems(["digitized slide", "Option C2", "Option C3"])

        # Blazer ID input (alphanumeric only)
        self.blazer_input = QLineEdit()
        self.blazer_input.setPlaceholderText("e.g., ab1234")
        regex = QRegularExpression("^[a-zA-Z0-9]+$")
        validator = QRegularExpressionValidator(regex)
        self.blazer_input.setValidator(validator)

        self.checkbox1 = QCheckBox("Enable feature X")
        self.checkbox2 = QCheckBox("Enable feature Y")

        self.submit_button = QPushButton("Submit")

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(QApplication.instance().quit)

        self.label.setFont(QFont('Calibri', 11, QFont.Bold))
        self.label2.setFont(QFont('Calibri', 11, QFont.Bold))
        self.label3.setFont(QFont('Calibri', 11, QFont.Bold))
        self.label4.setFont(QFont('Calibri', 11, QFont.Bold))
        self.label5.setFont(QFont('Calibri', 11, QFont.Bold))


        # --- Layout ---
        layout = QVBoxLayout()

        layout.addWidget(self.title_label, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Create a horizontal layout
        row_layout1 = QHBoxLayout()
        row_layout1.addWidget(self.label)
        row_layout1.addWidget(self.text_input)
        layout.addLayout(row_layout1)

        row_layout2 = QHBoxLayout()
        row_layout2.addWidget(self.label2)
        row_layout2.addWidget(self.text_input2)
        layout.addLayout(row_layout2)

        row_layout3 = QHBoxLayout()
        row_layout3.addWidget(self.label3)
        row_layout3.addWidget(self.dropdown1)
        layout.addLayout(row_layout3)

        row_layout4 = QHBoxLayout()
        row_layout4.addWidget(self.label4)
        row_layout4.addWidget(self.dropdown2)
        layout.addLayout(row_layout4)

        row_layout5 = QHBoxLayout()
        row_layout5.addWidget(self.label5)
        row_layout5.addWidget(self.dropdown3)
        layout.addLayout(row_layout5)

        row_layout = QHBoxLayout()
        row_layout.addWidget(QLabel("Blazer ID:"))
        row_layout.addWidget(self.blazer_input)
        # Add the horizontal layout to the vertical layout
        layout.addLayout(row_layout)


        row_layout6 = QHBoxLayout()
        row_layout6.addWidget(self.checkbox1)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleForm()
    window.show()
    sys.exit(app.exec())
