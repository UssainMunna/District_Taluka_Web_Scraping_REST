from flask import Flask,request,render_template
from flask import jsonify 
from app_config import fech_taluk,fetch_village,fetch_districts,count_districts,count_taluks,count_villages,insert_district
from helper import organize_the_all_data,fetch_all_query,fetch_one_query,insert_query

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    # Fetch all data from the respective tables using cursor
    districts = fetch_all_query(fetch_districts)
    print(districts)
    taluks = fetch_all_query(fech_taluk)
    villages = fetch_all_query(fetch_village)
    data = organize_the_all_data(districts,taluks,villages)
    # Return the JSON response using jsonify
    return jsonify(data)

@app.route('/count', methods=['GET'])
def get_count():
    #count of districts
    count_dis = fetch_one_query(count_districts)
    distict_count = count_dis[0]
    #count of taluk
    count_taluk = fetch_one_query(count_taluks)
    taluk_count = count_taluk[0]
    #count of villages
    count_village = fetch_one_query(count_villages)
    village_count = count_village[0]

    return jsonify({
        "District Count": distict_count,
        "Taluk Count": taluk_count,
        "Villages Count": village_count,
    })


@app.route('/add_district', methods=['POST'])
def add_district():
    data = request.get_json()
    district_name = data.get('district_name')
    if not district_name:return jsonify({"message": "District name is required."}), 400
    values = (district_name)
    insert_query(insert_district,values)
    return jsonify({"message": "District added successfully."}), 201


@app.route('/add_taluk', methods=['POST'])
def add_taluk():
    data = request.get_json()
    taluk_name = data.get('taluk_name')
    district_id = data.get('district_id')
    if not taluk_name or not district_id:return jsonify({"message": "Taluk name and District ID are required."}), 400
    try:
        query = "INSERT INTO Taluk_one (TalukName, DistrictId) VALUES (?, ?)"
        values = (taluk_name, district_id)
        insert_query(query,values)
        return jsonify({"message": "Taluk added successfully."}), 201
    except:return jsonify({"message": "District Id Not Existed."}), 400
    
    
@app.route('/add_village', methods=['POST'])
def add_village():
    data = request.get_json()
    village_name = data.get('village_name')
    taluk_id = data.get('taluk_id')
    district_id = data.get('district_id')

    if not village_name or not taluk_id or not district_id:
        return jsonify({"message": "Village name, Taluk ID, and District ID are required."}), 400
    try:
        query = "INSERT INTO Village_one (VillageName, TalukId, DistrictId) VALUES (?, ?, ?)"
        values = (village_name, taluk_id, district_id)        
        insert_query(query,values)
        return jsonify({"message": "Village added successfully."}), 201
    except:return jsonify({"message": "District Id or Taluk Not Existed."}), 400


@app.route('/delete_district/<int:district_id>', methods=['DELETE'])
def delete_district(district_id):
    try:
        query = "DELETE FROM District_one WHERE DistrictId = ?"
        values = (district_id,)
        insert_query(query,values)
        return jsonify({"message": "Taluk deleted successfully."}), 200
    except:return jsonify({"message" : "Village and Taluk should be deleted first" }),400

@app.route('/delete_taluk/<int:taluk_id>', methods=['DELETE'])
def delete_taluk(taluk_id):
    try:
        query = "DELETE FROM Taluk_one WHERE TalukId = ?"
        values = (taluk_id,)
        insert_query(query,values)
        return jsonify({"message": "Taluk deleted successfully."}), 200
    except:return jsonify({"message" : "Village should be deleted first" }),400

@app.route('/delete_village/<int:village_id>', methods=['DELETE'])
def delete_village(village_id):
    try:
        query = "DELETE FROM Village_one WHERE VillageId = ?"
        values = (village_id,)
        insert_query(query,values)
        return jsonify({"message": "Village deleted successfully."}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Village not exist."}), 400



if __name__ == '__main__':
    app.run(debug=True)