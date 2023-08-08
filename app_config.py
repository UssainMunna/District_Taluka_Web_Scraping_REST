fetch_districts= 'SELECT DistrictId, DistrictName FROM District_one'
fech_taluk = 'SELECT TalukId, TalukName, DistrictId FROM Taluk_one'
fetch_village = 'SELECT VillageId, VillageName, TalukId FROM Village_one'
count_districts = "SELECT COUNT(*) FROM District_one;"
count_taluks = "SELECT COUNT(*) FROM Taluk_one;"
count_villages = "SELECT COUNT(*) FROM Village_one;"
insert_district = f"INSERT INTO District_one (DistrictName) VALUES (?)"