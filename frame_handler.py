from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget, QHeaderView
)
from PySide6.QtCore import QDir, Qt
import os


class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter)

        self.table_view = QTableWidget()
        self.table_view.setColumnCount(3)
        self.table_view.setHorizontalHeaderLabels(["Ad", "Boyut (KB)", "Tür"])
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        splitter.addWidget(self.table_view)

        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setPlaceholderText("Terminal burada görüntülenecek...")
        splitter.addWidget(self.terminal)

        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)

        self.load_directory(QDir.homePath())

        self.table_view.itemDoubleClicked.connect(self.on_item_double_clicked)

    def load_directory(self, directory):
        self.table_view.setRowCount(0) 
        dir_obj = QDir(directory)
        dir_obj.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)

        for entry in dir_obj.entryInfoList():
            row_position = self.table_view.rowCount()
            self.table_view.insertRow(row_position)

            self.table_view.setItem(row_position, 0, QTableWidgetItem(entry.fileName()))
            size = entry.size() // 1024 if not entry.isDir() else "-"
            self.table_view.setItem(row_position, 1, QTableWidgetItem(str(size)))
            entry_type = "Directory" if entry.isDir() else "File"
            self.table_view.setItem(row_position, 2, QTableWidgetItem(entry_type))

    def on_item_double_clicked(self, item):
        row = item.row()
        file_name = self.table_view.item(row, 0).text()
        current_dir = QDir(self.table_view.windowFilePath()).path() if self.table_view.windowFilePath() else QDir.homePath()
        full_path = os.path.join(current_dir, file_name)

        if os.path.isdir(full_path):
            self.load_directory(full_path)
            self.terminal.append(f"File selected: {full_path}")
        else:
            self.terminal.append(f"File selected: {full_path}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = FileExplorer()
    window.show()
    sys.exit(app.exec())
