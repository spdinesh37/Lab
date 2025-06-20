from PySide6.QtCore import QObject, Signal

class Worker(QObject):
    progress = Signal(int)   # Signal to send progress (0-100)
    finished = Signal()      # Signal to notify task completion

    def run(self):
        # --- Start of run method ---
        self.start_method()  # Code to run at the very start

        # Main long-running task: pass progress.emit as callback
        your_long_task(self.progress.emit)

        self.end_method()    # Code to run at the very end

        self.finished.emit()  # Notify that the worker has finished
        # --- End of run method ---

    def start_method(self):
        # Code to execute right before starting the long task
        print("Starting the long task...")

    def end_method(self):
        # Code to execute right after finishing the long task
        print("Long task finished!")

def your_long_task(progress_callback):
    total_steps = 100
    for i in range(total_steps + 1):
        # --- Do part of the task here ---
        progress_callback(i)  # Update progress bar
        # --- End of step ---
