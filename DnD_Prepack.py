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

import Progress

USER_OS = system()


from PySide6.QtCore import QObject, Signal, QThread

class Worker(QObject):
    progress = Signal(int)
    finished = Signal(bool)
    error = Signal(str)

    def __init__(self, task_generator_func):
        super().__init__()
        self.task_generator_func = task_generator_func

    def run(self):
        try:
            for pct in self.task_generator_func():
                self.progress.emit(pct)
            self.finished.emit(True)
        except Exception as e:
            self.error.emit(str(e))
            self.finished.emit(False)



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

    def user_home(self):
        user_os = system()
        if not user_os == 'Windows':
            userHome = getenv('HOME')
        else:
            userHome = getenv('USERPROFILE')
        return userHome

    def check_filenames(self, chk_folder):
        """Checks to see if file names are properly formed. If it finds a
        malformed file name it notifies the User which filename caused the error
        and returns False.
        """
        for filename in listdir(chk_folder):
            # Checks file names, ignores folder names and hidden files
            if not os.path.splitext(filename)[1] == '' and not filename.startswith('.'):
                pattern = r"^[A-Z][A-Z][A-Z][A-Z]_[A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9][a|b]"
                test = path.splitext(filename)[0]
                if not len(test) == 20 or not match(pattern, test):
                    QMessageBox.warning(self, "Warning",
                                        "The file name {filename} is improperly\nformed. Quitting.".format(
                                            filename=filename))
                    return False
        return True

    def collate_files_(self):
        ignored_files = []
        total_files = 0
        included_files = 0
        info = self.l
        in_dir = info[0]
        good_filenames = False
        good_filenames = self.check_filenames(in_dir)
        if not good_filenames:
            return False
        p_dir = info[1]
        obj_list = []
        objects = path.join(p_dir, 'ready_to_package')
        if not path.isdir(objects):
            try:
                mkdir(objects)
            except:
                QMessageBox.warning(self, "Warning", "There was an error creating the \'ready_to_package\' folder.")
                return False
        for i,files in listdir(in_dir):

            # ignore directories/ folders
            if not path.splitext(files)[1] == '':
                total_files += 1
            accepted_files = ['.tif', '.pdf', '.xml', '.txt', '.jpg', '.iso', '.jp2', '.wav', '.mp4', '.mkv', '.mp3',
                              '.csv']
            yield int((i + 1) / total_files * 100)

            # script only accepts file formats of the proper type that do not begin with '.'
            if path.splitext(files)[1] not in accepted_files or files.startswith('.'):
                if not path.splitext(files)[1] == '' and not files.startswith('.'):
                    ignored_files.append(files)
            if path.splitext(files)[1] in accepted_files and not files.startswith('.'):
                included_files += 1
                oldfilepath = path.join(in_dir, files)
                itemname = files[0:-10]
                itemfolder = path.join(objects, itemname)
                if not itemname in obj_list:
                    obj_list.append(itemname)
                    try:
                        mkdir(itemfolder)
                    except FileExistsError:
                        yesno = True  # messagebox.askyesno(message=f'The folder {itemfolder} already exists!\nOverwrite?')
                        if yesno == True:
                            rmtree(itemfolder)
                            mkdir(itemfolder)
                        else:
                            quitting = True  # messagebox.askyesno(message=f'Do you want to quit?')
                            if quitting:
                                return False
                if files[-5] == 'a':
                    newfilepath = path.join(itemfolder, files)
                    try:
                        copy2(oldfilepath, newfilepath)
                    except:
                        QMessageBox.warning(self, "Warning", "There was an error copying:\n{files}")
                elif files[-5] == 'b':
                    newfilepath = path.join(itemfolder, files)
                    try:
                        copy2(oldfilepath, newfilepath)
                    except:
                        QMessageBox.warning(self, "Warning", "There was an error copying:\n{files}")
                else:
                    QMessageBox.warning(self, "Warning",
                                        "The filename {files} does not \nend in \'a\' or \'b\'.\nSkipping it...")
        QMessageBox.information(self, "Info",
                                "Found {} total files.\nCollated {} files.\nIgnored the following:\n{}".format(
                                    total_files, included_files, ignored_files))
        return True

    def check_ids(self, checkdir):
        for folder_id in listdir(checkdir):
            id_path = path.join(checkdir, folder_id)
            if path.isdir(id_path):
                pattern = r"^[A-Z][A-Z][A-Z][A-Z]_[A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][0-9][0-9]"
                if not match(pattern, folder_id):
                    return False
        return True

    def make_csv(self):
        csv_info = self.get_entries()
        proc_dir = csv_info[1]
        ownBy = csv_info[2]
        collection = csv_info[3]
        itemType = csv_info[4]
        username = csv_info[5]
        obj_dir = path.join(proc_dir, 'ready_to_package')
        if not path.isdir(obj_dir):
            QMessageBox.warning(self, "Warning", "Could not find the \"ready_to_package\" folder.\nQuitting.")
            return False
        out_dir = path.join(proc_dir, 'csv_loaders')
        if not path.isdir(out_dir):
            try:
                mkdir(out_dir)
            except:
                QMessageBox.warning(self, "Warning", "There was an error creating the \'csv_loaders\' folder.")
                return False
        datetime = time.strftime("%Y%b%d_%H%M%S")
        good_ids = False
        good_ids = self.check_ids(obj_dir)
        if good_ids == False:
            QMessageBox.warning(self, "Warning",
                                "One or more folders in target directory\nhave incorrect UUIDs. Quitting.")
            return False
        if USER_OS == 'Windows':
            try:
                newCSV = open(path.join(out_dir, f'csv_loader{datetime}.csv'), 'w', newline='', encoding='UTF-8')
            except:
                QMessageBox.warning(self, "Warning", "There was an error creating the CSV loader file.")
                return False
        else:
            try:
                newCSV = open(path.join(out_dir, f'csv_loader{datetime}.csv'), 'w', encoding='UTF-8')
            except:
                QMessageBox.warning(self, "Warning", "There was an error creating the CSV loader file.")
                return False
        colnames = ['System UUID', 'Local ID', 'Responsible Org', 'Collection', 'Item Type', 'Packaged By']
        writer = csv.writer(newCSV)
        writer.writerow(colnames)
        flist = listdir(obj_dir)
        sorted_flist = sorted(flist)
        numfolders = 0
        for dirs in sorted_flist:
            fpath = path.join(obj_dir, dirs)
            if path.isdir(fpath):
                newrow = ['unknown', 'unknown', 'unknown', 'unknown', 'unknown', 'unknown']
                newrow[0] = dirs
                newrow[1] = ''
                newrow[2] = ownBy
                newrow[3] = collection
                newrow[4] = itemType
                newrow[5] = username
                numfolders += 1
                writer.writerow(newrow)
        newCSV.close()
        QMessageBox.information(self, "Info", "Created CSV loader file\n with rows for {numfolders} items.")
        return True

    def run_procs(self):
        successful = False
        collate_yesno = self.feature_x.isChecked()
        csv_yesno = self.checkbox2.isChecked()
        if collate_yesno == 1:
            successful = self.collate_files_()
            if successful == False:
                QMessageBox.warning(self, "Warning", "Something went wrong during\ncollation. Quitting.")
                sys.exit()
        if csv_yesno == 1:
            successful = self.make_csv()
            if successful == False:
                QMessageBox.warning(self, "Warning", "Something went wrong during\nCSV Generation. Quitting.")
                sys.exit()
        else:
            QMessageBox.information(self, "Info", "Done!")
            sys.exit()



    def on_task_finished(self, success):
        self.progress_dialog.close()
        self.thread.quit()
        self.thread.wait()
        if success:
            QMessageBox.information(self, "Success", "Task completed successfully.")

    def on_task_error(self, msg):
        self.progress_dialog.close()
        QMessageBox.critical(self, "Error", f"An error occurred:\n{msg}")



    def start_task(self, task_func):
        self.progress_dialog = QProgressDialog("Processing...", None, 0, 100, self)
        self.progress_dialog.setWindowTitle("Working")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)
        self.progress_dialog.setValue(0)

        self.thread = QThread()
        self.worker = Worker(task_func)
        self.worker.moveToThread(self.thread)

        self.worker.progress.connect(self.progress_dialog.setValue)
        self.worker.finished.connect(self.on_task_finished)
        self.worker.error.connect(self.on_task_error)

        self.thread.started.connect(self.worker.run)
        self.thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleForm()
    window.show()
    sys.exit(app.exec())
