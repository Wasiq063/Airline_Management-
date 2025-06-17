# Connection details for database (Change here to run for specific database)
def connection_details():
    SERVER_NAME = 'WASIQS-PC\SQLSERVER1'
    DATABASE_NAME = 'ProjectDatabase'
    USERNAME = 'sa'
    PASSWORD = 'Fall2023.dbms'
    use_windows_authentication = True
    return SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, use_windows_authentication