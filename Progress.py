from PySide6.QtCore import QObject, Signal
from Collate_files import Collate_files

class Worker(QObject):
    progress = Signal(int)
    finished = Signal()
    error = Signal(str, str)   # title, message
    info = Signal(str, str)    # title, message

    def __init__(self, formData=None):
        super().__init__()
        self.formData = formData
        self.collator = Collate_files()

        # Connect collator signals to worker signals
        self.collator.error.connect(self.error)
        self.collator.info.connect(self.info)

    def run(self):
        self.collator.run_procs(self.progress.emit, self.formData)
        self.finished.emit()
