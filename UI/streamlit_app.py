import streamlit as st
import requests

# Set the title
st.title("Car Details Input Form")

# Fuel Type selection
fuel_type = st.selectbox(
    "Select Fuel Type",
    options=["CNG", "Petrol", "Diesel", "Electric", "LPG"]
)

# Build Type selection
build_type = st.selectbox(
    "Select Build Type",
    options=["Coupe", "Convertible", "Hatchback", "Hybrid", "MUV", "Minivan", "Pickup Truck", "SUV", "Sedan", "Wagon"]
)

# Transmission Type selection
transmission = st.selectbox(
    "Select Transmission Type",
    options=["Automatic", "Manual"]
)

# KM driven range input
# km_driven = st.slider(
#     "KM Driven",
#     min_value=0,
#     max_value=500000,
#     value=10000,
#     step=1000
# )

# KM driven input
km_driven = st.number_input(
    "KM Driven",
    min_value=1,
    max_value=351066,
    value=1,
    step=1
)

# Max Owners input
max_owner = st.number_input(
    "Maximum Owners",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)

# Number of seats input
seats = st.number_input(
    "Number of Seats",
    min_value=2,
    max_value=10,
    value=4,
    step=1
)

# Engine Displacement input
engine_displacement = st.number_input(
    "Engine Displacement (cc)",
    min_value=500,
    max_value=5000,
    value=1500,
    step=100
)

# Mileage input
mileage = st.number_input(
    "Mileage (kmpl)",
    min_value=5.0,
    max_value=50.0,
    value=15.0,
    step=0.1
)

# Max poewr input
max_power = st.number_input(
    "Max Power (bhp)",
    min_value=40.0,
    max_value=150.0,
    value=40.0,
    step=1.0
)

# Max poewr input
torque = st.number_input(
    "Torque (Nm)",
    min_value=69.0,
    max_value=270.0,
    value=69.0,
    step=1.0
)

# Max poewr input
car_age = st.number_input(
    "Car Age (years)",
    min_value=0,
    max_value=25,
    value=1,
    step=1
)


# # Submit button
# if st.button("Submit"):
#     st.write("### Car Details Submitted")
#     st.write("**Fuel Type**:", fuel_type)
#     st.write("**Build Type**:", build_type)
#     st.write("**Transmission**:", transmission)
#     st.write("**KM Driven**:", km_driven)
#     st.write("**Maximum Owners**:", max_owner)
#     st.write("**Number of Seats**:", seats)
#     st.write("**Engine Displacement (cc)**:", engine_displacement)
#     st.write("**Mileage (kmpl)**:", mileage)

# Button to trigger the API call
if st.button("Predict Price"):
    request = {}
    request['km'] = km_driven
    request['ownerNo'] = max_owner
    request['Seats'] = seats
    request['Engine Displacement'] = engine_displacement
    request['Mileage'] = mileage
    request['Max Power'] = max_power
    request['Torque'] = torque

    request["fuel_type"] = fuel_type
    request["build_type"] = build_type
    request["transmission"] = transmission
    request["car_age"] = car_age
    try:
        # Make the POST request to the Flask API endpoint
        response = requests.post("http://127.0.0.1:5001/predictrf", json=request)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("response",response)
            prediction = response.json().get("predicted val", "No price returned")
            st.success(f"The predicted car price is: ₹{prediction}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

    # You can add more logic here to process the submitted data or perform further actions.
    # make http post request with above data to server
    # server will return the price of the car
    # display the price of the car


    



    

