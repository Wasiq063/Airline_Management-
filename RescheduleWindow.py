from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
import pyodbc as odbc
from ConnectionString import connection_details


class RescheduleWindow(QtWidgets.QMainWindow):
    def __init__(self, selected_data, emp_id):
        super(RescheduleWindow, self).__init__()
        uic.loadUi('UI_Files/statusWindow.ui', self)
        self.setWindowTitle('Reschedule Window')
        self.show()
        self.emp_id = emp_id
        self.flight_no = selected_data
        
        # populate combobox
        self.populate_combobox()

        # buttons functionality
        self.statusOkayButton_2.clicked.connect(self.close_win)
        self.statusOkayButton.clicked.connect(self.complete_rescheduling)
        
    def populate_combobox(self):
        delays = ['15 min', '30 min', '1 hour', '2 hours', '4 hours', '1 day']
        self.comboBox.addItems(delays)

    def complete_rescheduling(self):
        delay = self.comboBox.currentText()  # Get the selected delay option
        # Establish the connection
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        conn = odbc.connect(connection_string)
        # Create a cursor
        cursor = conn.cursor()
        delay_by = delay.split()  # Get the numeric value of the delay

        if(delay_by[1] == 'min'):  # Delay in minutes
            query = """
            UPDATE Flights
            SET DepartureTime = DATEADD(MINUTE, ?, DepartureTime), ArrivalTime = DATEADD(MINUTE, ?, ArrivalTime), [Status] = 'Delayed'
            WHERE FlightNumber = ?;
            """

        elif(delay_by[1] == 'day'):  # Delay by one day
            query = """
            UPDATE Flights
            SET DepartureDate = DATEADD(DAY, ?, DepartureDate), ArrivalDate = DATEADD(DAY, ?, ArrivalDate), [Status] = 'Delayed'
            WHERE FlightNumber = ?;
            """

        else:  # Delay in hours
            query = """
            UPDATE Flights
            SET DepartureTime = DATEADD(HOUR, ?, DepartureTime), ArrivalTime = DATEADD(HOUR, ?, ArrivalTime), [Status] = 'Delayed'
            WHERE FlightNumber = ?;
            """
        
        
        # Execute query
        cursor.execute(query, (int(delay_by[0]), int(delay_by[0]), self.flight_no[0]))
        # Commit the transaction
        conn.commit()

        # update last updated by
        query = """
        UPDATE Flights
        SET LastUpdatedByID = ?
        WHERE FlightNumber = ?;
        """
        cursor.execute(query, (self.emp_id, self.flight_no[0]))
        conn.commit()
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        QMessageBox.information(self, "Success", "Flight delayed successfully.")
        self.close_win()


    def close_win(self):
        from FlightManagement import FlightManagement
        self.prev_win = FlightManagement(self.emp_id)
        self.close()
        self.prev_win.show()


    