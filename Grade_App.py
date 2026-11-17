import sys
import csv
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                               QTableWidget, QTableWidgetItem, QLineEdit, 
                               QVBoxLayout, QHBoxLayout, QFileDialog,QDialog,QLabel)
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtCore import Qt, QUrl 

class GradeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grade Correction App")
        self.resize(600, 500)

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.btn_load = QPushButton("Load File")
        self.btn_load.clicked.connect(self.load_file)
        layout.addWidget(self.btn_load)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(['ID', 'Original Grades', 'Corrected Grades'])
        layout.addWidget(self.table)

        h_layout = QHBoxLayout()
        self.input_points = QLineEdit()
        self.input_points.setPlaceholderText("Enter bonus points...")
        self.input_points.returnPressed.connect(self.apply_bonus)
        h_layout.addWidget(self.input_points)

        self.btn_update = QPushButton("Update File")
        self.btn_update.clicked.connect(self.update_file)
        h_layout.addWidget(self.btn_update)

        layout.addLayout(h_layout)

        self.btn_about = QPushButton("About")
        self.btn_about.clicked.connect(self.show_about)
        layout.addWidget(self.btn_about)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_name:
            self.selected_file = file_name
            self.student_ids.clear()
            self.original_grades.clear()
            
            with open(self.selected_file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        self.student_ids.append(row[0])
                        self.original_grades.append(float(row[1]))

            self.corrected_grades = list(self.original_grades)
            self.update_table()

    def update_table(self):
        for i in range(len(self.student_ids)):
            self.table.setItem(i, 0, QTableWidgetItem(str(self.student_ids[i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.original_grades[i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.corrected_grades[i])))

    def apply_bonus(self):
        try:
            bonus = int(self.input_points.text())
            for i in range(len(self.original_grades)):
                new_grade = self.original_grades[i] + bonus
                if new_grade > 100:
                    new_grade = 100.0
                self.corrected_grades[i] = new_grade
            self.update_table()
        except ValueError:
            pass

    def update_file(self):
        if not self.selected_file:
            return
        
        with open(self.selected_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Grade'])
            for i in range(len(self.student_ids)):
                writer.writerow([self.student_ids[i], self.corrected_grades[i]])

        os.startfile(self.selected_file)

    def show_about(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About")
        dialog.resize(300, 350)
        
        layout = QVBoxLayout(dialog)
        
        lbl_img = QLabel()
        pixmap = QPixmap("spongbob.jpg")
        if not pixmap.isNull():
            lbl_img.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            lbl_img.setText("Profile Image")
        lbl_img.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_img)
        
        lbl_email = QLabel("Email: ziv.Taieb@s.afeka.ac.il")
        lbl_email.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_email)
        
        btn_linkedin = QPushButton("LinkedIn Profile")
        btn_linkedin.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("www.linkedin.com/in/ziv-taieb-604192316")))
        layout.addWidget(btn_linkedin)
        
        btn_github = QPushButton("GitHub Repository")
        btn_github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/zivtaieb/Task-4.git")))
        layout.addWidget(btn_github)
        
        dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GradeApp()
    window.show()
    sys.exit(app.exec())