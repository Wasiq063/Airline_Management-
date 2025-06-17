from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate
import pyodbc as odbc
from ConnectionString import connection_details
from datetime import datetime


class AddManualWindow(QtWidgets.QMainWindow):
    def __init__(self, emp_id):
        super(AddManualWindow, self).__init__()
        uic.loadUi('UI_Files/addFlightManuallyWindow.ui', self)
        self.setWindowTitle('Add Flight Window')
        self.show()
        self.emp_id = emp_id
        self.addManualClose.clicked.connect(self.closeWindow)
        self.addWindowOkay.clicked.connect(self.addflight)
        self.default_date = QDate(2024, 1, 1)
    
    def addflight(self):
        # setting up server
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        f_from = self.from_Edit.text()
        f_to = self.to_Edit.text()
        dept_date = self.dept_date.date().toString("yyyy-MM-dd")
        dept_time = self.dept_time.time().toString("HH:mm:ss")
        arrival_date = self.arrival_date.date().toString("yyyy-MM-dd")
        arrival_time = self.arr_time.time().toString("HH:mm:ss")
        
        
        input_dept_date = datetime.strptime(dept_date, "%Y-%m-%d").date()
        input_arrival_date = datetime.strptime(arrival_date, "%Y-%m-%d").date()
        current_date = datetime.now().date()
        valid = (
            f_from and f_to and
            input_dept_date >= current_date and
            (input_arrival_date > input_dept_date or 
            (input_arrival_date == input_dept_date and arrival_time > dept_time))
        )

        if(valid):
            from FlightManagement import FlightManagement
            query = """
            INSERT INTO Flights ([From], [To], DepartureDate, ArrivalDate, DepartureTime, ArrivalTime, [Status], SeatsAvailable, TicketPrice, Availability)
            VALUES (?, ?, ?, ?, ?, ?, 'Scheduled', ?, ?, ?);
            """

            cursor.execute(query, (f_from, f_to, input_dept_date, input_arrival_date, dept_time, arrival_time, 12, 3000, 1))

            # Commit the changes to the database
            conn.commit()

            # Display success message
            QMessageBox.information(self, "Success", "Flight added successfully!")

            cursor.close()
            conn.close()
            self.flightmanagementwindow = FlightManagement(self.emp_id)
            self.closeWindow()
            self.flightmanagementwindow.show()
        else:
            self.showError("Wrong information entered!")
    
    def showError(self, message):
        # Display error message using QMessageBox
        error_message_box = QMessageBox(self)
        error_message_box.setIcon(QMessageBox.Icon.Critical)
        error_message_box.setText(message)
        error_message_box.setWindowTitle("Error")
        error_message_box.exec()

    def closeWindow(self):
        from FlightManagement import FlightManagement
        self.close()
        self.flightmanagementwindow = FlightManagement(self.emp_id)
        self.flightmanagementwindow.show()
