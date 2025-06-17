from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidget
import pyodbc as odbc
from ConnectionString import connection_details
from datetime import date

class CheckStatus(QtWidgets.QMainWindow):
    def __init__(self, email, password):
        super(CheckStatus, self).__init__()
        self.email = email
        self.password = password
        uic.loadUi('UI_Files/trackingwindow.ui', self)
        self.setWindowTitle('Flight Status')
        self.show()
        self.trackBack.clicked.connect(self.goBack)
        self.trackSearch.clicked.connect(self.RetrieveFlight)
        self.populateWindow()
        
    
    def goBack(self):
        from ProfileWindow import ProfileWindow
        self.close()
        self.prevWindow = ProfileWindow(self.email, self.password)
        self.prevWindow.show()

    def RetrieveFlight(self):
        flightNum = self.flightSearchCombo.currentText()
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT CustomerID
        FROM CustomerInfo 
        WHERE Email = ? AND Password = ?
        """, (self.email, self.password))
        customerID = int(cursor.fetchone()[0]) 
        if flightNum == "All Flights":
            cursor.execute("""
            SELECT F.FlightNumber, F.DepartureDate, F.ArrivalDate, F.DepartureTime, F.ArrivalTime, F.Status
            FROM Bookings B
            INNER JOIN Flights F ON B.FlightNumber = F.FlightNumber
            WHERE B.CustomerID = ?
            ORDER BY F.FlightNumber ASC
            """, customerID)
            data = cursor.fetchall()
            self.flightDetailTable.setRowCount(len(data))
            self.flightDetailTable.setColumnCount(len(data[0]))
            for row_idx,row in enumerate(data):
                for col_idx,col in enumerate(row):
                    if isinstance(col, date):
                        col = str(col).split('-')
                        col = f'{col[2]}-{col[1]}-{col[0]}'
                    self.flightDetailTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col)))
        else:
            flightNum = int(flightNum)
            cursor.execute("""
            SELECT F.FlightNumber, F.DepartureDate, F.ArrivalDate, F.DepartureTime, F.ArrivalTime, F.Status
            FROM Bookings B
            INNER JOIN Flights F ON B.FlightNumber = F.FlightNumber
            WHERE B.CustomerID = ? AND B.FlightNumber = ?
            """, (customerID, flightNum))
            data = cursor.fetchall()
            self.flightDetailTable.setRowCount(len(data))
            self.flightDetailTable.setColumnCount(len(data[0]))
            for row_idx,row in enumerate(data):
                for col_idx,col in enumerate(row):
                    if isinstance(col, date):
                        col = str(col).split('-')
                        col = f'{col[2]}-{col[1]}-{col[0]}'
                    self.flightDetailTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col)))

    def populateWindow(self):

        # Populating table with data of booked flights for specific customer
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT CustomerID
        FROM CustomerInfo 
        WHERE Email = ? AND Password = ?
        """, (self.email, self.password))
        customerID = int(cursor.fetchone()[0]) 
        cursor.execute("""
        SELECT F.FlightNumber, F.DepartureDate, F.ArrivalDate, F.DepartureTime, F.ArrivalTime, F.Status
        FROM Bookings B
        INNER JOIN Flights F ON B.FlightNumber = F.FlightNumber
        WHERE B.CustomerID = ?
        ORDER BY F.FlightNumber ASC
        """, customerID)
        data = cursor.fetchall()
        if data != []:
            self.flightDetailTable.setRowCount(len(data))
            self.flightDetailTable.setColumnCount(len(data[0]))
            for row_idx,row in enumerate(data):
                for col_idx,col in enumerate(row):
                    if isinstance(col, date):
                        col = str(col).split('-')
                        col = f'{col[2]}-{col[1]}-{col[0]}'
                    self.flightDetailTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col)))

        # Populating combo box with flight numbers of booked flights 
        cursor.execute("""
        SELECT FlightNumber
        FROM Bookings
        WHERE CustomerID = ?
        """, customerID)
        flightNums = cursor.fetchall()
        newFlightNums = []
        for flightNum in flightNums:
            if flightNum[0] not in newFlightNums:
                newFlightNums.append(int(flightNum[0]))
        newFlightNums = sorted(newFlightNums)
        for i in range(len(newFlightNums)):
            newFlightNums[i] = str(newFlightNums[i])
        newFlightNums = newFlightNums + ["All Flights"]
        self.flightSearchCombo.addItems(newFlightNums)
        conn.close()
