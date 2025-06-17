from PyQt6 import QtWidgets, uic


class Startup(QtWidgets.QMainWindow):
    def __init__(self):
        super(Startup, self).__init__()
        uic.loadUi('UI_Files/startupWindow.ui', self)
        self.setWindowTitle('Airline Management System')
        self.show()
        self.pushButton.clicked.connect(self.openCustLogin)
        self.pushButton_2.clicked.connect(self.openEmpLogin)

    def openEmpLogin(self):   #Opens Employee Login Window
        from EmployeeLogin import EmployeeLogin
        self.close()
        self.empLoginWindow = EmployeeLogin()
        self.empLoginWindow.show()

    def openCustLogin(self):  #Opens Customer Login Window
        from CustomerLogin import CustomerLogin
        self.close()
        self.custLoginWindow = CustomerLogin()
        self.custLoginWindow.show()









        