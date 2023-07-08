import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QDialog, QMessageBox, QVBoxLayout, QFormLayout, QDateEdit ,QComboBox
from PyQt5.QtCore import Qt, QDate, pyqtSignal, QObject
from PyQt5.QtGui import QIntValidator

class Communicate(QObject):
    form_submitted = pyqtSignal(str, str, str, str, str, str, str)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Aplikasi Pembuatan Paspor")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        form_layout = QFormLayout()

        self.label_name = QLabel("Nama:")
        self.lineedit_name = QLineEdit()

        self.label_address = QLabel("Alamat:")
        self.lineedit_address = QLineEdit()

        self.label_country = QLabel("Negara:")
        self.lineedit_country = QLineEdit()


        self.lineedit_gender = QLabel("Jenis Kelamin:")
        self.combo_box_gender = QComboBox(self)
        self.combo_box_gender.addItem("Laki-laki")
        self.combo_box_gender.addItem("Perempuan")


        self.label_birthdate = QLabel("Tanggal Lahir:")
        self.dateedit_birthdate = QDateEdit()
        self.dateedit_birthdate.setDisplayFormat("dd/MM/yyyy")
        self.dateedit_birthdate.setDate(QDate.currentDate())

        self.label_expired = QLabel("Expired:")
        self.dateedit_expired = QDateEdit()
        self.dateedit_expired.setDisplayFormat("dd/MM/yyyy")
        self.dateedit_expired.setDate(QDate.currentDate().addYears(10))

        self.label_registration = QLabel("Nomor Registrasi(hanya bisa di isi angka):")
        self.lineedit_registration = QLineEdit()
        self.lineedit_registration.setValidator(QIntValidator())
        form_layout.addRow(self.label_name, self.lineedit_name)
        form_layout.addRow(self.label_address, self.lineedit_address)
        form_layout.addRow(self.label_country, self.lineedit_country)
        form_layout.addRow(self.lineedit_gender,self.combo_box_gender)
        form_layout.addRow(self.label_birthdate, self.dateedit_birthdate)
        form_layout.addRow(self.label_expired, self.dateedit_expired)
        form_layout.addRow(self.label_registration, self.lineedit_registration)

        layout.addLayout(form_layout)

        self.button_submit = QPushButton("Submit")
        self.button_submit.clicked.connect(self.submit_form)
        layout.addWidget(self.button_submit)

        self.communicate = Communicate()
        self.communicate.form_submitted.connect(self.show_success_dialog)

    def submit_form(self):
        name = self.lineedit_name.text()
        address = self.lineedit_address.text()
        country = self.lineedit_country.text()
        gender =self.combo_box_gender.currentText()
        birthdate = self.dateedit_birthdate.date().toString(Qt.ISODate)
        expired = self.dateedit_expired.date().toString(Qt.ISODate)
        registration = self.lineedit_registration.text()

        if name and address and country and gender and birthdate and expired and registration:
            self.communicate.form_submitted.emit(name, address, country, gender, birthdate, expired, registration)
        else:
            QMessageBox.warning(self, "Peringatan", "Mohon isi semua kolom.")

    def show_success_dialog(self, name, address, country, gender, birthdate, expired, registration):
        dialog = QDialog(self)
        dialog.setWindowTitle("Sukses")
        dialog.setGeometry(100, 100, 400, 300)

        label_success = QLabel("Pembuatan paspor untuk {} dengan alamat {} berhasil.\n"
                               "Negara: {}\n"
                               "Jenis Kelamin: {}\n"
                               "Tanggal Lahir: {}\n"
                               "Expired: {}\n"
                               "Nomor Registrasi: {}".format(name, address, country, gender, birthdate, expired, registration))
        label_success.setAlignment(Qt.AlignLeft)
        label_success.setStyleSheet(
            """
            QLabel {
                background-image: url('background_image.jpg');
                background-repeat: no-repeat;
                background-position: center;
                color: black;
                font-size: 30px;
                padding: 20px;
            }
            """
        )

        layout = QVBoxLayout(dialog)
        layout.addWidget(label_success)

        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
