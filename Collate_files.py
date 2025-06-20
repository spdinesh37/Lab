import sys
import time
from os import listdir, path, mkdir
from re import match
from shutil import rmtree, copy2

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox


class Collate_files(QObject):
    error = Signal(str, str)  # Signal sending (title, message) strings


    def run_procs(self, progress_callback, formData):
        time.sleep(1)
        if progress_callback:
            progress_callback(100*1)
        successful = False
        print(formData.toString())
        collate_yesno = formData.to_string_list()
        csv_yesno = formData.feature_y
        if collate_yesno == 1:
            time.sleep(1)
            if progress_callback:
                progress_callback(100 * 2)
            successful = self.collate_files(formData)
            time.sleep(1)
            if progress_callback:
                progress_callback(100 * 3)
            if successful == False:
                self.error.emit(
                    "Warning",  # Window title
                    "Something went wrong during\ncollation. Quitting."
                )
            return
        if csv_yesno == 1:
            time.sleep(1)
            if progress_callback:
                progress_callback(100 * 4)
            successful = self.make_csv()
            if successful == False:
                self.error.emit(  # assuming you're inside a QWidget/QMainWindow subclass
                    "Warning",
                    "Something went wrong during\nCSV Generation. Quitting."
                )
                return
        else:
            time.sleep(1)
            if progress_callback:
                progress_callback(100 * 5)
            QMessageBox.information(
                None ,  # parent widget, or use None if not in a QWidget
                "Info",  # title of the dialog
                "Done!"  # message text
            )
            return

    def check_ids(self, checkdir):
        # use self to silence the static warning, e.g.:
        _ = self  # dummy usage
        for folder_id in listdir(checkdir):
            id_path = path.join(checkdir, folder_id)
            if path.isdir(id_path):
                pattern = r"^[A-Z][A-Z][A-Z][A-Z]_[A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][0-9][0-9]"
                if not match(pattern, folder_id):
                    return False
        return True

    def check_filenames(self, chk_folder):
        """Checks to see if file names are properly formed. If it finds a
        malformed file name it notifies the User which filename caused the error
        and returns False.
        """
        for filename in listdir(chk_folder):
            # Checks file names, ignores folder names and hidden files
            if not path.splitext(filename)[1] == '' and not filename.startswith('.'):
                pattern = r"^[A-Z][A-Z][A-Z][A-Z]_[A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9][a|b]"
                test = path.splitext(filename)[0]
                if not len(test) == 20 or not match(pattern, test):
                    self.error.emit( # your QWidget or None
                        "Warning",
                        f"The file name {filename} is improperly\nformed. Quitting."
                    )
                    return False
        return True

    def collate_files(self, formData):

        ignored_files = []
        total_files = 0
        included_files = 0
        info = self.get_entries()
        print(info.keys())
        in_dir = info[0]
        good_filenames = False
        good_filenames = self.check_filenames(in_dir)
        if good_filenames == False:
            return False
        p_dir = info[1]
        obj_list = []
        objects = path.join(p_dir, 'ready_to_package')
        if not path.isdir(objects):
            try:
                mkdir(objects)
            except:
                self.error.emit(  # parent widget (or None)
                    "Warning",  # dialog title
                    "There was an error creating the 'ready_to_package' folder."
                )
                return False
        for files in listdir(in_dir):
            # ignore directories/ folders
            if not path.splitext(files)[1] == '':
                total_files += 1
            accepted_files = ['.tif', '.pdf', '.xml', '.txt', '.jpg', '.iso', '.jp2', '.wav', '.mp4', '.mkv', '.mp3',
                              '.csv']
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
                        reply = QMessageBox.question(
                            self,  # parent widget, or None
                            "Confirm Overwrite",  # dialog title
                            f"The folder {itemfolder} already exists!\nOverwrite?",  # message
                            QMessageBox.Yes | QMessageBox.No  # buttons
                        )

                        if reply == QMessageBox.Yes:
                            yesno = True
                        else:
                            yesno = False
                        if yesno == True:
                            rmtree(itemfolder)
                            mkdir(itemfolder)
                        else:
                            reply = QMessageBox.question(
                                self,  # parent widget or None
                                "Confirm Exit",  # dialog title
                                "Do you want to quit?",  # message text
                                QMessageBox.Yes | QMessageBox.No
                            )

                            quitting = (reply == QMessageBox.Yes)
                            if quitting == True:
                                return False
                if files[-5] == 'a':
                    newfilepath = path.join(itemfolder, files)
                    try:
                        copy2(oldfilepath, newfilepath)
                    except:
                        self.error.emit(  # parent widget or None
                            "Warning",
                            f"There was an error copying:\n{files}"
                        )
                elif files[-5] == 'b':
                    newfilepath = path.join(itemfolder, files)
                    try:
                        copy2(oldfilepath, newfilepath)
                    except:
                        self.error.emit(  # parent widget, usually 'self'
                            "Warning",  # dialog title
                            f"There was an error copying:\n{files}"  # message text
                        )

                else:
                    QMessageBox.warning(
                        self,  # your QWidget parent or None
                        "Warning",
                        f"There was an error copying:\n{files}"
                    )
        self.error.emit(
            "Info",
            f"Found {total_files} total files.\nCollated {included_files} files.\nIgnored the following:\n{ignored_files}"
        )
        return True

