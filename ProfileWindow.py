from PyQt6 import QtWidgets, uic
import pyodbc as odbc
from ConnectionString import connection_details
from PyQt6.QtWidgets import QTableWidget

class ProfileWindow(QtWidgets.QMainWindow):
    def __init__(self, email, password):
        super(ProfileWindow, self).__init__()
        uic.loadUi('UI_Files/profileWindow.ui', self)
        self.setWindowTitle('Profile Window')
        self.show()
        self.email = email
        self.password = password
        self.nameEdit.setEnabled(False)
        self.emailEdit.setEnabled(False)
        self.passportEdit.setEnabled(False)
        self.cnicEdit.setEnabled(False)
        self.custIDEdit.setEnabled(False)
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)

        # Create a cursor and execute the query
        cursor = conn.cursor()
        cursor.execute("""
        SELECT Name, Email, PassportNumber, CNIC, CustomerID
        FROM CustomerInfo
        WHERE Email = ? AND Password = ?
        """, (self.email, self.password))
        result = cursor.fetchone()
        conn.close()
        if result:
            self.nameEdit.setText(str(result[0]))
            self.emailEdit.setText(str(result[1]))
            self.passportEdit.setText(str(result[2]))
            self.cnicEdit.setText(str(result[3]))
            self.custIDEdit.setText(str(result[4]))
        else:
            self.goBack()

        self.populateTable()
        self.checkStatusButton.clicked.connect(self.openTrackingWindow)
        self.profileBack.clicked.connect(self.goBack)
        self.bookButton.clicked.connect(self.openBookingWindow)

    def openBookingWindow(self):
        from BookingWindow import BookingWindow
        self.close()
        self.bookingWindow = BookingWindow(self.email, self.password)
        self.bookingWindow.show()
    
    def openTrackingWindow(self):
        from CheckStatus import CheckStatus
        self.close()
        self.trackingWindow = CheckStatus(self.email, self.password)
        self.trackingWindow.show()

    def goBack(self):
        from CustomerLogin import CustomerLogin
        self.close()
        self.prevWindow = CustomerLogin()
        self.prevWindow.show()

    def populateTable(self):
        customerID = int(self.custIDEdit.text())
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)

        self.bookedFlightsTable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        cursor = conn.cursor()
        cursor.execute("""
        SELECT F.FlightNumber, TicketID, B.SeatNumber, [From], [To], DepartureDate, ArrivalDate, DepartureTime, ArrivalTime
        FROM Bookings B
        INNER JOIN Flights F ON B.FlightNumber = F.FlightNumber
        WHERE B.CustomerID = ?
        ORDER BY F.FlightNumber ASC
        """, customerID)
        data = cursor.fetchall()
        if data != []:
            self.bookedFlightsTable.setRowCount(len(data))
            self.bookedFlightsTable.setColumnCount(len(data[0]))
            for row_idx,row in enumerate(data):
                for col_idx,col in enumerate(row):
                    self.bookedFlightsTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col)))
        conn.close()
