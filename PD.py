from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar

class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processing")
        self.setFixedSize(300, 100)
        self.setModal(True)

        layout = QVBoxLayout()
        self.label = QLabel("Processing, please wait...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
