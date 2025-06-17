from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from ConnectionString import connection_details
import pyodbc as odbc

class CustomerLogin(QtWidgets.QMainWindow):
    def __init__(self):
        super(CustomerLogin, self).__init__()
        uic.loadUi('UI_Files/customerLogin.ui', self)
        self.setWindowTitle('Credential Entry')
        self.show()
        self.pushButton_2.clicked.connect(self.login)
        self.pushButton_3.clicked.connect(self.openSignUp)
        self.pushButton_4.clicked.connect(self.goBack)

    def openProfileWindow(self, email, password):
        from ProfileWindow import ProfileWindow
        self.close()
        self.profileWindow = ProfileWindow(email, password)
        self.profileWindow.show()


    def openSignUp(self):
        from SignUpWindow import SignUpWindow
        self.close()
        self.signUpForm = SignUpWindow()
        self.signUpForm.show()
    
    def goBack(self):
        from Startup import Startup
        self.close()
        self.prevWindow = Startup()
        self.prevWindow.show()

    def showError(self, message):
        # Display error message using QMessageBox
        error_message_box = QMessageBox(self)
        error_message_box.setIcon(QMessageBox.Icon.Critical)
        error_message_box.setText(message)
        error_message_box.setWindowTitle("Error")
        error_message_box.exec()

    def check_credentials(self, username, password):
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("select Email, Password from CustomerInfo")
        data = cursor.fetchall()
        conn.close()
        for row in data:
            if (row[0] == username and row[1] == password):
                return True
        return False
    
    def login(self):
        email = self.customerLineEdit.text()
        password = self.customerPasswordEdit.text()
        if self.check_credentials(email, password):
            self.openProfileWindow(email, password)
        else:
            self.showError("Incorrect Username or Password")
    
        