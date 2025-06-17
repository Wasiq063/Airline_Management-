from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from ManagementOptions import ManagementOptions
import pyodbc as odbc
from ConnectionString import connection_details
from datetime import date


class PassengerWindow(QtWidgets.QMainWindow):
    def __init__(self, emp_id):
        super(PassengerWindow, self).__init__()
        uic.loadUi('UI_Files/passengerInfo.ui', self)
        self.setWindowTitle('Passenger Information')
        self.show()
        self.emp_id = emp_id
        self.populatecomboBox()
        self.passengerSearch.clicked.connect(self.populatetable)
        self.passengerBack.clicked.connect(self.goBack)

    def populatetable(self):
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        
        flight_number = self.comboBox.currentText()
        
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        
        if flight_number == "" and self.customerComboBox.currentText() == "":
            cursor.execute("""
            SELECT DISTINCT C.Name, C.PassportNumber, C.CNIC, F.FlightNumber,F.DepartureDate, F.ArrivalDate, F.DepartureTime, F.ArrivalTime
            FROM Bookings B
            INNER JOIN Flights F ON B.FlightNumber = F.FlightNumber 
            INNER JOIN CustomerInfo C on C.CustomerID = B.CustomerID
            """)
            data = cursor.fetchall()

        elif flight_number != "" and self.customerComboBox.currentText() == "":
            flight_number = int(flight_number)
            cursor.execute("""
            SELECT DISTINCT C.Name, C.PassportNumber, C.CNIC, F.FlightNumber,F.DepartureDate, F.ArrivalDate, F.DepartureTime, F.ArrivalTime
            FROM Bookings B
            INNER JOIN Flights F ON B.FlightNumber = F.FlightNumber 
            INNER JOIN CustomerInfo C on C.CustomerID = B.CustomerID
            WHERE B.FlightNumber = ?
            """, (self.comboBox.currentText()))
            data = cursor.fetchall()
        
        elif flight_number != "" and self.customerComboBox.currentText() != "":
            flight_number = int(flight_number)
            cursor.execute("""
            SELECT DISTINCT C.Name, C.PassportNumber, C.CNIC, F.FlightNumber,F.DepartureDate, F.ArrivalDate, F.DepartureTime, F.ArrivalTime
            FROM Bookings B
            INNER JOIN Flights F ON B.FlightNumber = F.FlightNumber 
            INNER JOIN CustomerInfo C on C.CustomerID = B.CustomerID
            WHERE B.FlightNumber = ? AND B.CustomerID = ?
            """, (flight_number, int(self.customerComboBox.currentText())))
            data = cursor.fetchall()

        elif flight_number == "" and self.customerComboBox.currentText() != "":
            self.showError("Please select a flight number")
            conn.close()
            return
        
        conn.close()
        if data != []:
                self.passengerTable.setRowCount(len(data))
                self.passengerTable.setColumnCount(len(data[0]))
                for row_idx,row in enumerate(data):
                    for col_idx,col in enumerate(row):
                        if isinstance(col, date):
                            col = str(col).split('-')
                            col = f'{col[2]}-{col[1]}-{col[0]}'
                        self.passengerTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col)))
        else:
            self.passengerTable.setRowCount(0)  
            self.passengerTable.setColumnCount(8) 


    def showError(self, message):
        # Display error message using QMessageBox
        error_message_box = QMessageBox(self)
        error_message_box.setIcon(QMessageBox.Icon.Critical)
        error_message_box.setText(message)
        error_message_box.setWindowTitle("Error")
        error_message_box.exec()

    def populatecomboBox(self):
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)
        # Create a cursor and execute the query
        cursor = conn.cursor()
        cursor.execute("select FlightNumber from Flights")
        self.comboBox.addItem("")
        for row in cursor.fetchall():
            self.comboBox.addItem(str(row[0]))
        cursor.execute("""
        SELECT CustomerID 
        FROM CustomerInfo
        """)
        customerIDs = cursor.fetchall()
        customerIDs = sorted(customerIDs)
        self.customerComboBox.addItem("")
        for row in customerIDs:
            self.customerComboBox.addItem(str(row[0]))
        conn.close()
        

    def goBack(self):
        self.close()
        self.prevWindow = ManagementOptions(self.emp_id)
        self.prevWindow.show()
        
