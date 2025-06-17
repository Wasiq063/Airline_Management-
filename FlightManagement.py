from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidget,QMessageBox
import pyodbc as odbc
from ConnectionString import connection_details

    
class FlightManagement(QtWidgets.QMainWindow):
    def __init__(self, emp_id):
        super(FlightManagement, self).__init__()
        uic.loadUi('UI_Files/addDeleteReschedule.ui', self)
        self.setWindowTitle('Flight Management')
        self.show()
        self.emp_id = emp_id
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.refresh_table()

        self.addFlightButton.clicked.connect(self.openAddFlightWindow)
        self.rescheduleButton.clicked.connect(self.openRescheduleWindow)
        self.addDeleteBack.clicked.connect(self.goBack)
        self.addManuallyButton.clicked.connect(self.openAddManualWindow)
        self.cancelFlightButton.clicked.connect(self.delete_flight)


    def delete_flight(self):
        selected_row = self.tableWidget.selectionModel().selectedRows()
        selected_flight = [
            self.tableWidget.item(index.row(), 1).text()  # Get first column of the row
            for index in selected_row
        ]
        if selected_flight:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setWindowTitle("Confirm Deletion")
            msg.setText(f"Are you sure you want to delete flight {selected_flight[0]}?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            # Get the user's response
            response = msg.exec()
            if response == QMessageBox.StandardButton.Yes:
                self.perform_deletion(selected_flight[0], self.emp_id)
                self.refresh_table()
            else:
                msg.close()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a flight before proceeding.")



    def refresh_table(self):
        # Establish the connection
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)

        # Create a cursor and execute the query
        cursor = conn.cursor()
        cursor.execute("select LastUpdatedByID, FlightNumber, [From], [To], DepartureDate, ArrivalDate, DepartureTime, ArrivalTime, Status from Flights where [Availability] = 1")
        data = cursor.fetchall()
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        # Enable row selection
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        for row_idx,row in enumerate(data):
            for col_idx,col in enumerate(row):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col)))
        
    def perform_deletion(self, flight_no, emp_id):
        flight_no = int(flight_no)
        # Establish the connection to the database
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'

        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        # retrieve ticket price
        query = """SELECT TicketPrice
        FROM Flights
        WHERE FlightNumber = ?
        """
        cursor.execute(query, flight_no)
        ticket_price = cursor.fetchall()[0][0]

        # Retrieve and update the balance for each customer who booked seats on the flight
        query = """
        SELECT CustomerID, COUNT(*) AS SeatCount
        FROM Bookings
        WHERE FlightNumber = ?
        GROUP BY CustomerID
        """
        cursor.execute(query, flight_no)
        customer_bookings = cursor.fetchall()

        for customer_id, seat_count in customer_bookings:
            refund_amount = ticket_price * seat_count

            # Update the customer's balance
            update_query = """
            UPDATE CustomerInfo
            SET Balance = Balance + ?
            WHERE CustomerID = ?
            """
            cursor.execute(update_query, refund_amount, customer_id)
        
        cursor.commit()

        # delete all bookings for the flight
        query = """
        DELETE FROM Bookings
        WHERE FlightNumber = ?
        """
        cursor.execute(query,flight_no)
        cursor.commit()

        # update flight from Flights table
        query = """        
        update Flights
        set [Availability] = 0, LastUpdatedByID = ?
        where FlightNumber = ?
        """
        cursor.execute(query, emp_id, flight_no)
        cursor.commit()
        QMessageBox.information(self, "Success", "Flight cancelled successfully.")
        cursor.close()
        conn.close()

    def goBack(self):
        from ManagementOptions import ManagementOptions
        self.close()
        self.prevWindow = ManagementOptions(self.emp_id)
        self.prevWindow.show()

    def openAddFlightWindow(self):
        from AddFlightWindow import AddFlightWindow
        self.addFlightWindow = AddFlightWindow(self.emp_id)
        self.close()
        self.addFlightWindow.show()

    def openRescheduleWindow(self):       
        from RescheduleWindow import RescheduleWindow
        #Get the selected rows
        selected_row = self.tableWidget.selectionModel().selectedRows()
        # Extract only the flight number
        selected_data = [
            self.tableWidget.item(index.row(), 1).text()  # Get first column of the row
            for index in selected_row
        ]
        if selected_data:
            from RescheduleWindow import RescheduleWindow
            self.reschedule_win = RescheduleWindow(selected_data, self.emp_id)
            self.close()
            self.reschedule_win.show()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a flight before proceeding.")

    def openAddManualWindow(self):
        from AddManualWindow import AddManualWindow
        self.close()
        self.addManualWindow = AddManualWindow(self.emp_id)
        self.addManualWindow.show()
