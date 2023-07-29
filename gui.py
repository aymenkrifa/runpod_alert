import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QDialog,
    QTimeEdit,
    QLabel,
    QVBoxLayout,
    QDialogButtonBox
)
from PyQt5.QtCore import Qt, QTime
from helpers import get_pod_info

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime(15, 0))

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select the new scheduled time:"))
        layout.addWidget(self.time_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_selected_time(self):
        return self.time_edit.time()


class PodStatusGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pod Status GUI")
        self.setGeometry(100, 100, 1100, 350)

        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(50, 50, 1000, 250)

        headers = ["CHECK TIME", "POD ID", "NAME", "GPU", "IMAGE NAME", "STATUS"]
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)

        self.refresh_button = QPushButton("Refresh", self)
        self.refresh_button.setGeometry(50, 310, 100, 30)
        self.refresh_button.clicked.connect(self.refresh_data)
        
        self.settings_button = QPushButton("Settings", self)
        self.settings_button.setGeometry(170, 310, 100, 30)
        self.settings_button.clicked.connect(self.open_settings_dialog)

        self.refresh_data()

    def add_pod_data(self, pod_list):
        if not pod_list:
            self.table_widget.setRowCount(1)
            item = QTableWidgetItem("No pod is currently running")
            item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(0, 0, item)
            self.table_widget.setSpan(0, 0, 1, self.table_widget.columnCount())
        else:
            self.table_widget.setRowCount(len(pod_list))
            for row, pod in enumerate(pod_list):
                for col, key in enumerate(pod.keys()):
                    value = pod[key]
                    item = QTableWidgetItem(str(value))
                    self.table_widget.setItem(row, col, item)

        self.table_widget.resizeColumnsToContents()
    
    def open_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        if settings_dialog.exec_() == QDialog.Accepted:
            selected_time = settings_dialog.get_selected_time()

    def refresh_data(self):
        pod_list = get_pod_info()
        self.add_pod_data(pod_list)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PodStatusGUI()
    window.show()
    sys.exit(app.exec_())
