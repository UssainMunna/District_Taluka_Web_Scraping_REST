import pyodbc

server = "mssql.esmsys.in,14251"
database = "interview"
username = "interview"
password = "Interview@123"
conn = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}")

# Combine the data and append related IDs
def organize_the_all_data(districts,taluks,villages):
    data = []
    for district in districts:
        district_data = {
            'DistrictId': district[0],
            'DistrictName': district[1],
            'Taluks': []}
        for taluk in taluks:
            if taluk[2] == district[0]:
                taluk_data = {
                    'TalukId': taluk[0],
                    'TalukName': taluk[1],
                    'Villages': []
                }
                for village in villages:
                    if village[2] == taluk[0]:
                        village_data = {
                            'VillageId': village[0],
                            'VillageName': village[1]
                        }
                        taluk_data['Villages'].append(village_data)

                district_data['Taluks'].append(taluk_data)
        data.append(district_data)
    return data

def fetch_all_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def fetch_one_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result

def insert_query(query,values):
    cursor = conn.cursor()
    cursor.execute(query,values)
    cursor.commit()
    cursor.close()