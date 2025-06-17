from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from ProfileWindow import ProfileWindow
from ConnectionString import connection_details
import pyodbc as odbc

class SignUpWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SignUpWindow, self).__init__()
        uic.loadUi('UI_Files/signup_form.ui', self)
        self.setWindowTitle('Sign-up Form')
        self.show()
        self.signUpBack.clicked.connect(self.goBack)
        self.signUpOkay.clicked.connect(self.createAccount)

    def goBack(self):
        from CustomerLogin import CustomerLogin
        self.close()
        self.prevWindow = CustomerLogin()
        self.prevWindow.show()
        

    def openProfileWindow(self, email, password):
        from ProfileWindow import ProfileWindow
        self.close()
        self.profileWindwow = ProfileWindow(email, password)
        self.profileWindwow.show()
    
           
    def showError(self, message):
        # Display error message using QMessageBox
        error_message_box = QMessageBox(self)
        error_message_box.setIcon(QMessageBox.Icon.Critical)
        error_message_box.setText(message)
        error_message_box.setWindowTitle("Error")
        error_message_box.exec()

    def createAccount(self):
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)

        # Create a cursor and execute the query
        cursor = conn.cursor()

        name = self.nameSign.text()
        email = self.emailSign.text()
        password = self.passSign.text()
        passportNum = self.passportSign.text()
        cnic = self.cnicSign.text()

        if cnic == "" or name == "" or password == "" or email == "":
            self.showError("Please enter correct credentials (Passport Number is optional).") 
            self.goBack()
        else:
            if passportNum == "":
                passportNum = None
            cursor.execute("""
            INSERT INTO CustomerInfo(Name, Email, Password, PassportNumber, CNIC)
            VALUES (?, ?, ?, ?, ?)
            """, name, email, password, passportNum, cnic)
            conn.commit()
            self.openProfileWindow(email, password)  # Opening profile window for the new account     
            conn.close()
        

