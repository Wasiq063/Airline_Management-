
import pyodbc
import random
from datetime import datetime, timedelta


# Utility functions

def randomEmail(name):
    domains = ['@gmail.com', '@yahoo.com', '@outlook.com']
    firstName = name.split(" ")[0].lower()
    lastName = name.split(" ")[1].lower()
    choice = random.randint(0,2)
    return f"{lastName}.{firstName}{domains[choice]}"

def randomPassword(name):  # Gets ASCII value of first name and joins with last name to generate unique password
    firstName = name.split(" ")[0].lower()
    lastName = name.split(" ")[1].lower()
    result = random.randint(1000,2000)
    for j in range(len(firstName)):
        result += ord(firstName[j])
    return f"{lastName}{str(result)}"

def randomCNIC():
    return f"42501-{str(random.randint(1000000,9999999))}-{str(random.randint(0,9))}"

def randomPassportNum():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    startingLetters = random.choices(letters, k = 2)
    return f"{startingLetters[0]}{startingLetters[1]}{str(random.randint(1000000,9999999))}"


# Database creation function

def createDatabase(SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication):

    #Establishing connection with database 
    if use_windows_authentication:
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
    else:
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cities = [
        "Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta", "Multan", "Faisalabad", 
        "Rawalpindi", "Hyderabad", "Sialkot", "Gujranwala", "Bahawalpur", "Skardu"
    ] 

    employee_names = [
    "Ayesha Khan",
    "Hassan Ali",
    "Fatima Siddiqui",
    "Ahmed Qureshi",
    "Zara Malik",
    "Omar Sheikh",
    "Noor Javed",
    "Saad Raza",
    "Nadia Iqbal",
    "Imran Hussain"
    ]

    customer_names = [
    "Sara Khan",
    "Bilal Ahmed",
    "Mariam Farooq",
    "Usman Malik",
    "Amina Sheikh",
    "Arham Raza",
    "Zainab Hussain",
    "Tariq Siddiqui",
    "Naila Javed",
    "Shahid Qureshi"
    ]

    # Creating database

    cursor.execute("""
    CREATE TABLE EmployeesInfo(
        EmployeeID INT IDENTITY(1,1) PRIMARY KEY,
        EmployeeName VARCHAR(50) NOT NULL,
        Email VARCHAR(50) UNIQUE NOT NULL,
        Password VARCHAR(50) NOT NULL);                    
    """)
    
    cursor.execute("""
    CREATE TABLE CustomerInfo(
        CustomerID INT IDENTITY(1,1) PRIMARY KEY,
        Name VARCHAR(50) NOT NULL,
        Email VARCHAR(50) UNIQUE,
        Password VARCHAR(50) NOT NULL,
        PassportNumber VARCHAR(50),
        CNIC VARCHAR(50) NOT NULL,
        Balance INT NOT NULL DEFAULT 10000);                                
    """)


    cursor.execute("""
    CREATE TABLE Flights(
        FlightNumber INT IDENTITY(1,1) PRIMARY KEY,
        LastUpdatedByID INT DEFAULT NULL,
        [From] VARCHAR(50) NOT NULL,
        [To] VARCHAR(50) NOT NULL,
        DepartureDate DATE NOT NULL,
        ArrivalDate DATE NOT NULL,
        DepartureTime TIME NOT NULL,
        ArrivalTime TIME NOT NULL,
        SeatsAvailable INT NOT NULL DEFAULT 12,
        Status VARCHAR(50) NOT NULL DEFAULT 'Arriving on time',
        TicketPrice INT NOT NULL DEFAULT 3000,
        Availability BIT DEFAULT 1,
        FOREIGN KEY (LastUpdatedByID) REFERENCES EmployeesInfo(EmployeeID));                                
    """)


    cursor.execute("""
    CREATE TABLE Bookings(
        TicketID INT IDENTITY(1,1) PRIMARY KEY,
        SeatNumber INT NOT NULL,
        CustomerID INT NOT NULL,
        FlightNumber INT NOT NULL,
        FOREIGN KEY (FlightNumber) REFERENCES Flights(FlightNumber),
        FOREIGN KEY (CustomerID) REFERENCES CustomerInfo(CustomerID));                                   
    """)

    conn.commit()

    # Populating CustomerInfo table

    for name in customer_names:
        email = randomEmail(name)
        password = randomPassword(name)
        choice = random.randint(0,2)
        if choice == 1:
            passportNum = randomPassportNum()
        else:
            passportNum = None
        cnic = randomCNIC()
        cursor.execute("""
        INSERT INTO CustomerInfo(Name, Email, Password, PassportNumber, CNIC) 
        VALUES(?, ?, ?, ?, ?);
        """, name, email, password, passportNum, cnic) 

    #Populating EmployeesInfo table

    for name in employee_names:
        email = randomEmail(name)
        password = randomPassword(name)
        cursor.execute("""
        INSERT INTO EmployeesInfo(EmployeeName, Email, Password)
        VALUES(?, ?, ?)
        """, name, email, password)
    
    conn.commit()


    # Populating Flights table 

    now = datetime.now()
    for i in range(15):
        fromCity, toCity = random.sample(cities, 2)  # Picks two random cities from cities list
        deptDateTime = now + timedelta(days = random.randint(0,7), hours = random.randint(0,24), minutes = random.randint(0, 59), seconds = random.randint(0,59))
        arrivalDateTime = deptDateTime + timedelta(hours = random.randint(1, 3), minutes = random.randint(0, 59), seconds = random.randint(0, 59))
        deptDate = deptDateTime.date()
        deptTime = deptDateTime.time()
        arrivalDate = arrivalDateTime.date()
        arrivalTime = arrivalDateTime.time()
        cursor.execute("""
        INSERT INTO Flights([From], [To], DepartureDate, ArrivalDate, DepartureTime, ArrivalTime)
        VALUES(?, ?, ?, ?, ?, ?)
        """, fromCity, toCity, deptDate, arrivalDate, deptTime, arrivalTime)
    
    conn.commit()

    # Setting up some unavailable flights for testing

    cursor.execute("""
    UPDATE Flights
    SET [Availability] = 0
    WHERE FlightNumber = 3
    UPDATE Flights
    SET [Availability] = 0
    WHERE FlightNumber = 14
    UPDATE Flights
    SET [Availability] = 0
    WHERE FlightNumber = 7
    """)
    conn.commit()

    # PRE-DEFINED PROCEDURES:

    # Procedure to get all available flights with matching From and To destinations 
    cursor.execute("""
    CREATE PROCEDURE RetrieveFlights
        @fromDest VARCHAR(50), 
        @toDest VARCHAR(50) 
    AS
    BEGIN
        SELECT FlightNumber, DepartureDate, ArrivalDate, DepartureTime, ArrivalTime, TicketPrice
        FROM Flights
        WHERE [From] = @fromDest AND [To] = @toDest AND [Availability] = 1
    END;
    """)
    conn.commit()
    conn.close()





