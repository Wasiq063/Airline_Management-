from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
import pyodbc as odbc
from ConnectionString import connection_details

class EmployeeLogin(QtWidgets.QMainWindow):
    def __init__(self):
        super(EmployeeLogin, self).__init__()
        uic.loadUi('UI_Files/employeeLogin.ui', self)
        self.setWindowTitle('Credential Entry')
        self.show()
        self.pushButton_57.clicked.connect(self.login)
        self.pushButton_58.clicked.connect(self.goBack)
        
    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if self.check_credentials(username, password):
            self.openOptions()
        else:
            self.showError("Incorrect Username or Password")

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
        cursor.execute("select Email, Password from EmployeesInfo")
        for row in cursor.fetchall():
            if (row[0] == username and row[1] == password):
                return True
        return False

    def openOptions(self):
        from ManagementOptions import ManagementOptions
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        username = self.lineEdit.text()
        query = """
        SELECT EmployeeID
        FROM EmployeesInfo
        where Email = ?;
        """
        cursor.execute(query, username)
        emp_id = cursor.fetchall()[0][0]
        self.close()
        self.options = ManagementOptions(emp_id)
        self.options.show()

    def goBack(self):
        from Startup import Startup
        self.close()
        self.prevWindow = Startup()
        self.prevWindow.show()
        