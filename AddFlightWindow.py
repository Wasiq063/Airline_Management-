from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidget, QMessageBox
import pyodbc as odbc
from ConnectionString import connection_details

class AddFlightWindow(QtWidgets.QMainWindow):
    def __init__(self, emp_id):
        super(AddFlightWindow, self).__init__()
        uic.loadUi('UI_Files/addFlightWindow.ui', self)
        self.setWindowTitle('Add Flight Window')
        self.show()
        self.emp_id = emp_id

        self.populate_table_with_flights()
        
        
        self.addFlightClose.clicked.connect(self.closeWindow)
        self.pushButton_4.clicked.connect(self.addflight)

    def addflight(self):
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        if selected_rows:
            for row_index in selected_rows:
                row_data = [
                    self.tableWidget.item(row_index.row(), col).text()  # Get data from each column in the selected row
                    for col in range(self.tableWidget.columnCount())
                ]
            #establishing connection
            SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
            if use_windows_authentication:
                connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
            else:
                connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
            conn = odbc.connect(connection_string)
            cursor = conn.cursor()
            query = """
            update Flights
            set Availability = 1
            where FlightNumber = ?
            """
            cursor.execute(query, row_data[0])
            cursor.commit()

            # update last updated by
            query = """
            UPDATE Flights
            SET LastUpdatedByID = ?
            WHERE FlightNumber = ?
            """
            cursor.execute(query, (self.emp_id, row_data[0]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Flight availability updated successfully.")
            self.populate_table_with_flights()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a flight before proceeding.")

    def populate_table_with_flights(self):
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        query = """
        select FlightNumber, [From], [To], DepartureDate, ArrivalDate, DepartureTime, ArrivalTime
        from Flights
        where [Availability] = 0
        """
        cursor.execute(query)
        data = cursor.fetchall()
       
        if data:
            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(len(data[0]))
            # Enable row selection
            self.tableWidget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            for row_idx,row in enumerate(data):
                for col_idx,col in enumerate(row):
                    self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col)))
        else:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            QMessageBox.information(self, "No Data", "No flights were found.")
        

    def closeWindow(self):
        from FlightManagement import FlightManagement
        self.prev_win = FlightManagement(self.emp_id)
        self.close()
        self.prev_win.show()
