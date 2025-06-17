from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidget
import pyodbc as odbc
from ConnectionString import connection_details
from datetime import datetime, time, date
import random
from PyQt6.QtWidgets import QMessageBox, QWidget

class BookingWindow(QtWidgets.QMainWindow):
    def __init__(self, email, password):
        super(BookingWindow, self).__init__()
        self.email = email
        self.password = password
        uic.loadUi('UI_Files/bookingWindow.ui', self)
        self.setWindowTitle('Flight Booking')
        self.show()
        self.cities = [
        "Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta", "Multan", "Faisalabad", 
        "Rawalpindi", "Hyderabad", "Sialkot", "Gujranwala", "Bahawalpur", "Skardu"
        ] 
        self.bookingWindowTable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bookSeatButton.clicked.connect(self.bookSeat)
        self.fromComboBox.addItems(self.cities)
        self.fromComboBox.currentIndexChanged.connect(self.changeToCity)
        self.flightSearchButton.clicked.connect(self.RetrieveFlights)
        self.bookingBack.clicked.connect(self.goBack)



    def goBack(self):
        from ProfileWindow import ProfileWindow
        self.close()
        self.prevWindow = ProfileWindow(self.email, self.password)
        self.prevWindow.show()
    

    def bookSeat(self):

        # Populating the table
        data = []
        for row_idx in range(1):
            for col_idx in range(6):
                if self.bookingWindowTable.item(row_idx, col_idx):
                    data.append(self.bookingWindowTable.item(row_idx, col_idx).text())
        

        if data != []:
            flightNum = int(data[0])
            SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
            if use_windows_authentication:
                connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
            else:
                connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
            conn = odbc.connect(connection_string)
            cursor = conn.cursor()

            # Checking to see whether seats are available for the selected flight or not
            cursor.execute("""
            SELECT SeatsAvailable
            FROM Flights 
            WHERE FlightNumber = ? AND SeatsAvailable = 0
            """, flightNum)
            data = cursor.fetchone()
            if data != None:
                self.showError("No seats available for this flight.")
                return
            
            
            cursor.execute("""
            SELECT CustomerID
            FROM CustomerInfo 
            WHERE Email = ? AND Password = ?
            """, (self.email, self.password))

            customerID = int(cursor.fetchone()[0])  # Getting CustomerID for the specific customer            

            cursor.execute("""
            SELECT FlightNumber, SeatNumber
            FROM Bookings
            """)

            bookings = cursor.fetchall() 

            # The while loop below checks if a seat number has already been booked on the same flight or not, if so, a new seat number is assigned to that customer
            seatNumber = random.randint(30, 42)
            while True:
                seatTaken = False
                for booking in bookings:
                    if flightNum == int(booking[0]) and seatNumber == int(booking[1]):
                        seatTaken = True
                        break
                if seatTaken:
                    seatNumber = random.randint(30, 42)
                else:
                    break
                
            # Checking to ensure flights with a time clash cannot be booked
            cursor.execute("""
            SELECT DepartureDate, ArrivalDate, DepartureTime, ArrivalTime
            FROM Flights
            WHERE FlightNumber = ?
            """, flightNum)
            flightData = cursor.fetchone()

            deptDate, arrivalDate, deptTime, arrivalTime = flightData

            cursor.execute("""
            SELECT F.DepartureDate, F.ArrivalDate, F.DepartureTime, F.ArrivalTime
            FROM Bookings B
            INNER JOIN Flights F ON F.FlightNumber = B.FlightNumber
            WHERE B.CustomerID = ?
            """, customerID)
            bookingData = cursor.fetchall()

            for booking in bookingData:
                bookedDeptDate, bookedArrivalDate, bookedDeptTime, bookedArrivalTime = booking
                if (bookedDeptDate == deptDate and bookedDeptTime > deptTime and bookedDeptTime < arrivalTime) or (bookedArrivalDate == arrivalDate and bookedArrivalTime > deptTime and bookedArrivalTime < arrivalTime):
                    self.showError("Booking time clashes with a booked flight")
                    conn.close()
                    return 
                
            # Booking the flight and updating tables accordingly 
            cursor.execute("""
            UPDATE Flights
            SET SeatsAvailable = SeatsAvailable - 1
            WHERE FlightNumber = ?
            """, flightNum)

            cursor.execute("""
            INSERT INTO Bookings(SeatNumber, CustomerID, FlightNumber)
            VALUES (?, ?, ?)
            """, seatNumber, customerID, flightNum)
            conn.commit()

            window = QWidget()
            QMessageBox.information(window, "Information", "Flight has been booked", QMessageBox.StandardButton.Ok)
            window.show()
            conn.close()


    def showError(self, message):
        error_message_box = QMessageBox(self)
        error_message_box.setIcon(QMessageBox.Icon.Critical)
        error_message_box.setText(message)
        error_message_box.setWindowTitle("Error")
        error_message_box.exec()

    def changeToCity(self):
        self.toComboBox.clear()
        fromCity = self.fromComboBox.currentText()
        newCities = []
        for i in self.cities:
            if i != fromCity:
                newCities.append(i)
        self.toComboBox.addItems(newCities)
        
        
    def RetrieveFlights(self):
        fromCity = self.fromComboBox.currentText()
        toCity = self.toComboBox.currentText()
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("""
        EXEC RetrieveFlights @fromDest = ?, @toDest = ?
        """, (fromCity, toCity))
        data = cursor.fetchall()
        if data != []:
            self.bookingWindowTable.setRowCount(len(data))
            self.bookingWindowTable.setColumnCount(len(data[0]))
            for row_idx,row in enumerate(data):
                for col_idx,col in enumerate(row):
                    if isinstance(col, date):
                        col = str(col).split('-')
                        col = f'{col[2]}-{col[1]}-{col[0]}'
                    self.bookingWindowTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col)))
        else:
            self.bookingWindowTable.setRowCount(0)  
            self.bookingWindowTable.setColumnCount(6)  
        conn.close()
