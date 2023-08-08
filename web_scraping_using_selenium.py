import pyodbc
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

server = "mssql.esmsys.in,14251"
database = "interview"
username = "interview"
password = "Interview@123"

# Create a connection to the database
conn = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}")
cursor = conn.cursor()

def startBot():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.get("https://eservices.tn.gov.in/eservicesnew/land/chittaCheckNewRural_en.html?lan=en")
    driver.maximize_window()
    dis = driver.find_element(By.XPATH, "//select[@name='districtCode']").text
    Details = {}
    District_values = dis.split("t--")[1].split("\n")[1:]
    for i in District_values[20:40]:
        driver.find_element(By.XPATH, "//select[@name='districtCode']").send_keys(i)
        time.sleep(3)
        taluk = driver.find_element(By.XPATH, "//select[@name='talukCode']").text
        Taluk_values = taluk.split("k--")[1].split("\n")[1:]
        Taluk_dict = {}
        taluk_list = []
        for j in Taluk_values:
            driver.find_element(By.XPATH, "//select[@name='talukCode']").send_keys(j)
            time.sleep(3)
            village = driver.find_element(By.XPATH, "//select[@name='villageCode']").text
            Village_values = village.split("e--")[1].split("\n")[1:]
            Taluk_dict.update({j:Village_values})
        taluk_list.append(Taluk_dict)
        Details.update({i:taluk_list})
    return Details


def upload_to_db(data):
    for district_name, taluks in data.items():
        # Insert into District table
        insert_into_district = f"INSERT INTO District_one (DistrictName) VALUES ('{district_name}');"
        cursor.execute(insert_into_district)
        cursor.commit()
        district_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
        print("District:", district_name, "ID:", district_id)

        for taluk_info in taluks[0].items():
            taluk_name, villages = taluk_info
            #Insert into Taluk table
            insert_into_taluk = f"INSERT INTO Taluk_one (TalukName, DistrictId) VALUES ('{taluk_name}', {district_id})"
            cursor.execute(insert_into_taluk)
            cursor.commit()
            taluk_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
            print("Taluk:", taluk_name, "ID:", taluk_id)
            for village_name in villages:
                #Insert into Village table
                insert_into_village = f"INSERT INTO Village_one (VillageName, TalukId, DistrictId) VALUES ('{village_name}', {taluk_id}, {district_id});"
                cursor.execute(insert_into_village)
                cursor.commit()
                print("Village:", village_name)

#get the all district data from 
result_data = startBot()

#insert into database
upload_to_db(result_data)

# Close the connection
conn.close()
