import pickle
import streamlit as st
import pandas as pd

# from streamlit_option_menu import option_menu

user_input = {}
required_order = ['Miscellaneous_Gear Box', 'Year of Manufacture', 'Max Power', 'Torque',
                  'Mileage', 'Kms Driven', 'Transmission', 'model', 'city',
                  'Engine Displacement', 'Miscellaneous_Rear Brake Type',
                  'Miscellaneous_Tyre Type', 'Features', 'oem', 'Seats',
                  'Engine and Transmission_Fuel Suppy System', 'bt', 'ownerNo', 'Insurance Validity',
                  'Miscellaneous_Front Brake Type']

st.title("Welcome To Car price prediction Application")
with st.sidebar:
    st.write("You Can select the preferred options and calculate the car price")
    with open('mappings.pkl', 'rb') as file:
        mappings = pickle.load(file)
    for col, mapping in mappings.items():

        user_input[col] = st.selectbox(
            f"Select a {col}:",
            list(mapping.keys())  # Show original category names
        )
    encoded_inputs = {}
    for col, value in user_input.items():
        encoded_inputs[col] = mappings[col][value]

    km = [1000, 5000, 50000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 550000, 600000,
          650000, 700000, 750000, 800000, 850000, 900000, 950000, 1000000, 1050000, 1100000, 1150000, 1200000, 1250000,
          1300000, 1350000, 1400000, 1450000, 1500000, 1550000, 1600000, 1650000, 1700000, 1750000, 1800000, 1850000,
          1900000, 1950000, 2000000, 2050000, 2100000, 2150000, 2200000, 2250000, 2300000, 2350000, 2400000, 2450000,
          2500000, 2550000, 2600000, 2650000, 2700000, 2750000, 2800000, 2850000, 2900000, 2950000, 3000000, 3050000,
          3100000, 3150000, 3200000, 3250000, 3300000, 3350000, 3400000, 3450000, 3500000, 3550000, 3600000, 3650000,
          3700000, 3750000, 3800000, 3850000, 3900000, 3950000, 4000000, 4050000, 4100000, 4150000, 4200000, 4250000,
          4300000, 4350000, 4400000, 4450000, 4500000, 4550000, 4600000, 4650000, 4700000, 4750000, 4800000, 4850000,
          4900000, 4950000, 5000000, 5050000, 5100000, 5150000, 5200000, 5250000, 5300000, 5350000, 5400000, 5450000,
          5500000
          ]

    seats = [5, 7, 8, 6, 10, 4, 9, 2]
    gears = [9, 8, 4, 6, 5, 7, 1]
    owner = [3, 1, 2, 4, 0, 5]

    Km_input = st.selectbox(
        f"Select a Kms driven:",
        list(km)  # Show original category names
    )
    seat_input = st.selectbox(
        f"Select a No. of Seats:",
        list(seats)  # Show original category names
    )
    gears_input = st.selectbox(
        f"Select a No. of Gears:",
        list(gears)  # Show original category names
    )
    owner_input = st.selectbox(
        f"Select a No. of Owners:",
        list(owner)  # Show original category names
    )
    encoded_inputs['Kms Driven'] = Km_input
    encoded_inputs['Seats'] = seat_input
    encoded_inputs['Miscellaneous_Gear Box'] = gears_input
    encoded_inputs['ownerNo'] = owner_input
    print(encoded_inputs)

ordered_encoded_inputs = [encoded_inputs[col] for col in required_order]
input_data = pd.DataFrame([ordered_encoded_inputs], columns=required_order)
if st.button('Predict'):
    with open('best_model.pkl', 'rb') as file:
       result = pickle.load(file)
    # Predict using the model
    prediction = result.predict(input_data)

    # Display the prediction
    st.write(f"The predicted car price is: {prediction}")
