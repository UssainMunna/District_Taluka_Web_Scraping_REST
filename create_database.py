import pyodbc


# Database connection details
server = "mssql.esmsys.in,14251"
database = "interview"
username = "interview"
password = "Interview@123"

# Create a connection to the database

conn = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}")

cursor = conn.cursor()

def create_district(cursor):
    # Create three tables: District, Taluka, and Village
    create_district = """CREATE TABLE District_one (
                                DistrictId INT IDENTITY(1, 1) PRIMARY KEY,
                                DistrictName NVARCHAR(100) NOT NULL
                        );"""
    cursor.execute(create_district)
    conn.commit()
    conn.close()

def create_taluk(cursor):
    create_taluk = """CREATE TABLE Taluk_one (
                    TalukId INT IDENTITY(1, 1) PRIMARY KEY,
                    TalukName NVARCHAR(100) NOT NULL,
                    DistrictId INT NOT NULL,
                    FOREIGN KEY (DistrictId) REFERENCES District_one(DistrictId)
                    );"""
    # Create three tables: District, Taluka, and Village
    cursor.execute(create_taluk)
    conn.commit()
    conn.close()

def create_village(cursor):
    create_village_table ="""CREATE TABLE Village_one (
                    VillageId INT IDENTITY(1, 1) PRIMARY KEY,
                    VillageName NVARCHAR(100) NOT NULL,
                    TalukId INT NOT NULL,
                    DistrictId INT NOT NULL,
                    FOREIGN KEY (TalukId) REFERENCES Taluk_one(TalukId),
                    FOREIGN KEY (DistrictId) REFERENCES District_one(DistrictId)
                );"""
    cursor.execute(create_village_table)
    conn.commit()
    conn.close()
