# ✈️ Airline Management System

A desktop-based Airline Management System built with **Python**, **PyQt6** for the UI, and **Microsoft SQL Server** for the backend database using **pyodbc**. This project is designed to demonstrate database management, UI/UX design, and CRUD operations in a real-world flight booking context.

---

## 📁 Project Structure

This project consists of multiple modules handling everything from user authentication to booking and rescheduling flights.
-The UI directory contains all the UI file
-The main project directory contains all the python files

> ✅ On running `main.py`, the application will **automatically create the database** in SQL Server and populate it with sample data using SQL queries.

---

## 🧰 Features

- Customer and employee login portals
- Add, edit, reschedule and cancel flights
- Manual and dynamic flight data insertion
- Booking and check status modules
- Profile management
- Interactive PyQt6-based GUI
- SQL Server integration with sample flight data

---

## 💾 Installation

### Prerequisites:
- Python 3.10+
- Microsoft SQL Server (with authentication enabled)
- Git (to clone this repo)

### Step-by-step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/airline-management-system.git
   cd airline-management-system

---

## 🗃️ Database Details

- The application uses **Microsoft SQL Server** via **pyodbc** for connecting to the database.
- Upon first launch (by running `main.py`), it will:
  - Automatically **create the database** using `CreateDatabase.py`
  - Create required **tables and relationships**
  - Populate the system with **sample flight and user data**
- You can customize your **SQL Server credentials** in the `ConnectionString.py` file.

> ⚠️ Ensure that your SQL Server instance is running and that `TCP/IP` is enabled. If needed, update the `DRIVER`, `SERVER`, `UID`, and `PWD` values in the connection string to match your local configuration.

---

## 📫 Contact

For queries, collaboration, or feedback:  
**Wasiq Shaikh**  
📧 wasiqshaikh063@gmail.com   
💼 (https://www.linkedin.com/in/wasiq-shaikh-357565211/)) *(optional)*  

---
