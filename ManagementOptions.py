from PyQt6 import QtWidgets, uic


class ManagementOptions(QtWidgets.QMainWindow):
    def __init__(self, emp_id):
        super(ManagementOptions, self).__init__()
        uic.loadUi('UI_Files/managementOptions.ui', self)
        self.setWindowTitle('Management Options')
        self.show()
        self.emp_id = emp_id
        self.passengerInfoSelect.clicked.connect(self.openPassengerInfoWindow)
        self.flightManageSelect.clicked.connect(self.openFlightManagementWindow)
        self.managementBack.clicked.connect(self.goBack)

    def goBack(self):
        from EmployeeLogin import EmployeeLogin
        self.close()
        self.prevWindow = EmployeeLogin()
        self.prevWindow.show()

    def openPassengerInfoWindow(self):
        from PassengerWindow import PassengerWindow
        self.close()
        self.passengerWindow = PassengerWindow(self.emp_id)
        self.passengerWindow.show()

    def openFlightManagementWindow(self):
        from FlightManagement import FlightManagement
        self.close()
        self.managementWindow = FlightManagement(self.emp_id)
        self.managementWindow.show()