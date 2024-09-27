import json
import numpy as np
import pandas as pd
import xgboost as xgb
from flask import Flask, request, jsonify
import os
import joblib
# import pickle

# Load the XGBoost model
model = xgb.XGBRegressor()
model.load_model("model/xgboost_model_car_pred.json")  # Make sure your model is saved as xgboost_model.json


# Initialize Flask app
app = Flask(__name__)

# create a /health endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "flask healthy"})


expected_columns = ['km', 'ownerNo',  'Seats', 'Engine Displacement', 'Mileage',
       'Max Power', 'Torque', 'ft_Cng', 'ft_Diesel', 'ft_Electric', 'ft_Lpg',
       'ft_Petrol',  'bt_Convertibles', 'bt_Coupe', 'bt_Hatchback',
       'bt_Hybrids', 'bt_MUV', 'bt_Minivans', 'bt_Pickup Trucks', 'bt_SUV',
       'bt_Sedan', 'bt_Wagon', 'transmission_Automatic', 'transmission_Manual', 'Car_Age']


def get_df_from_request(request_json):

    df = pd.DataFrame()

    new_row = {}

    if request_json["fuel_type"] == "CNG":
        new_row["ft_Cng"] = 1
    if request_json["fuel_type"] == "Electric":
        new_row["ft_Electric"] = 1
    if request_json["fuel_type"] == "Petrol":
        new_row["ft_Petrol"] = 1
    if request_json["fuel_type"] == "LPG":
        new_row["ft_Lpg"] = 1
    if request_json["fuel_type"] == "Diesel":
        new_row["ft_Diesel"] = 1


    if request_json["build_type"] == "Coupe":
        new_row["bt_Coupe"] = 1
    if request_json["build_type"] == "Convertible":
        new_row["bt_Convertibles"] = 1
    if request_json["build_type"] == "Hatchback":
        new_row["bt_Hatchback"] = 1
    if request_json["build_type"] == "Hybrid":
        new_row["bt_Hybrids"] = 1
    if request_json["build_type"] == "MUV":
        new_row["bt_MUV"] = 1
    if request_json["build_type"] == "Minivan":
        new_row["bt_Minivans"] = 1
    if request_json["build_type"] == "Pickup Truck":
        new_row["bt_Pickup Trucks"] = 1
    if request_json["build_type"] == "SUV":
        new_row["bt_SUV"] = 1
    if request_json["build_type"] == "Sedan":
        new_row["bt_Sedan"] = 1
    if request_json["build_type"] == "Wagon":
        new_row["bt_Wagon"] = 1


    if request_json["transmission"] == "Automatic":
        new_row["transmission_Automatic"] = 1
    if request_json["transmission"] == "Manual":
        new_row["transmission_Manual"] = 1
    
    new_row["km"] = request_json["km"]
    new_row["ownerNo"] = request_json["ownerNo"]
    new_row["Seats"] = request_json["Seats"]
    new_row["Engine Displacement"] = request_json["Engine Displacement"]
    new_row["Mileage"] = request_json["Mileage"]
    new_row["Max Power"] = request_json["Max Power"]
    new_row["Torque"] = request_json["Torque"]
    new_row["Car_Age"] = request_json["car_age"]
    
    
    print("request_jso ca",request_json["car_age"])
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    return df

@app.route('/predictxg', methods=['POST'])
def predict():
    try:
        # Get the JSON data from the request
        request_json = request.json

        input_data = get_df_from_request(request_json)
        
        for col in expected_columns:
            if col not in input_data.columns:
                input_data[col] = 0  # Set a default value, e.g., 0 for missing columns

        input_data = input_data[expected_columns]

        json_input_data = input_data.to_json(orient='records')

        print("j",json_input_data)

        # # Make a prediction
        predicted_price = model.predict(input_data)
        print(f"Predicted Price: {predicted_price[0]}")
        return jsonify({"predicted val": str(predicted_price[0])}), 200  

    except Exception as e:
        print("error",e)
        return jsonify({"error": str(e)}), 400
    

@app.route('/predictrf', methods=['POST'])
def predictrf():
    try:
        req_ft = pd.DataFrame()
        req_df = pd.DataFrame()

        with open('model/random_forest_model.pkl', 'rb') as file:    
            rf_model_loaded = joblib.load(file)

            req_ft = get_df_from_request(request.json)

            for col in expected_columns:
                if col not in req_ft.columns:
                    req_df[col] = 0  # Set a default value, e.g., 0 for missing columns  
                else:
                    req_df[col] = req_ft[col]

            predictions = rf_model_loaded.predict(req_df)
            return jsonify({"predicted val": str(predictions[0])}), 200

    except Exception as e:
        print("error",e)
        return jsonify({"error": str(e)}), 400    

if __name__ == "__main__":
    # get port from env
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
