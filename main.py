import sys
from PyQt6 import QtWidgets
from Startup import Startup
from CreateDatabase import createDatabase
from ConnectionString import connection_details

# CHANGE CONNECTION DETAILS FOR DATABASE IN ConnectionString.py 

def main():  
    # Try-Except block to allow the database to be created only once when the program is run for the first time
    try:
        SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication = connection_details()
        createDatabase(SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication)
    except:
        pass
    app = QtWidgets.QApplication(sys.argv)
    # change to Startup
    window = Startup()
    app.exec() # Start the application

main()



