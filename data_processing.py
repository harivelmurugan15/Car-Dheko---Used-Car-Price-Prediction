import pandas as pd
import json


def preprocess_json(json_str):
    json_str = json_str.replace("'", '"')
    json_str = json_str.replace("None", "null")
    return json_str


def column_processing(df):
    # new_car_detail
    df['new_car_detail'] = df['new_car_detail'].apply(preprocess_json)
    df['json_data'] = df['new_car_detail'].apply(json.loads)

    json_df = pd.json_normalize(df['json_data'])

    df = df.drop(['new_car_detail', 'json_data'], axis=1).join(json_df)

    # new_car_overview
    df['new_car_overview'] = df['new_car_overview'].apply(preprocess_json)
    df['json_data1'] = df['new_car_overview'].apply(json.loads)

    car_overview = []

    for index in df['json_data1']:
        car_overview_data = pd.DataFrame([{item['key']: item['value'] for item in index['top']}])
        car_overview.append(car_overview_data)

    json_df1 = pd.concat(car_overview, ignore_index=True)
    df = df.drop(['new_car_overview', 'json_data1'], axis=1).join(json_df1)

    # new_car_feature
    df['new_car_feature'] = df['new_car_feature'].apply(preprocess_json)
    df['json_data2'] = df['new_car_feature'].apply(json.loads)

    car_features = []
    data_dict = {}

    for index in df['json_data2']:
        top_list = [item['value'] for item in index['top']]
        data_dict[index['heading']] = top_list

        for section in index['data']:
            heading = section['heading']
            values = [item['value'] for item in section['list']]
            if heading in data_dict:
                data_dict[heading].extend(values)
            else:
                data_dict[heading] = values

            car_feature_data = {k: ', '.join(v) for k, v in data_dict.items()}
        car_features.append(car_feature_data)

    json_df2 = pd.DataFrame(car_features)
    df = df.drop(['new_car_feature', 'json_data2'], axis=1).join(json_df2)

    # new_car_specs

    df['new_car_specs'] = df['new_car_specs'].apply(preprocess_json)
    df['json_data3'] = df['new_car_specs'].apply(json.loads)

    car_specs = []

    for index in df['json_data3']:
        specs_dict = {}
        for item in index['top']:
            specs_dict[item['key']] = item['value']

        for section in index['data']:
            heading = section['heading']
            for item in section['list']:
                col_key = f"{heading}_{item['key']}"
                specs_dict[col_key] = item['value']

        car_specs.append(specs_dict)

    json_df3 = pd.DataFrame(car_specs)
    df.rename(columns={'Seats': 'No_of_Seats'}, inplace=True)
    df = df.drop(['new_car_specs', 'json_data3'], axis=1).join(json_df3)
    df.drop(
        ['car_links', 'it', 'ft', 'km', 'transmission', 'modelYear', 'centralVariantId', 'owner', 'priceSaving',
         'priceFixedText',
         'trendingText.imgUrl', 'trendingText.heading', 'trendingText.desc', 'Registration Year', 'RTO', 'Ownership',
         'Engine', 'No_of_Seats',
         'Engine and Transmission_Displacement', 'Engine and Transmission_Max Power',
         'Engine and Transmission_Max Torque', 'Engine and Transmission_BoreX Stroke',
         'Dimensions & Capacity_Length', 'Dimensions & Capacity_Width', 'Dimensions & Capacity_Height',
         'Dimensions & Capacity_Wheel Base',
         'Dimensions & Capacity_Front Tread', 'Dimensions & Capacity_Rear Tread', 'Dimensions & Capacity_Kerb Weight',
         'Dimensions & Capacity_Gross Weight',
         'Miscellaneous_Seating Capacity', 'Miscellaneous_Turning Radius', 'Miscellaneous_Alloy Wheel Size',
         'Dimensions & Capacity_Ground Clearance Unladen', 'Engine and Transmission_Compression Ratio', 'priceActual',
         'Wheel Size', 'Engine and Transmission_Color',
         'Engine and Transmission_Engine Type', 'Engine and Transmission_Turbo Charger', 'Miscellaneous_Acceleration',
         'Engine and Transmission_Super Charger', 'variantName'], axis=1, inplace=True)

    return df


Kolkata_cars = pd.read_excel(r"C:\Users\ASUS\Downloads\kolkata_cars.xlsx")
new_Kolkata_cars = column_processing(Kolkata_cars)
new_Kolkata_cars['city'] = 'Kolkata'
new_Kolkata_cars.to_excel("new_Kolkata_cars.xlsx")

hyderabad_cars = pd.read_excel(r"C:\Users\ASUS\Downloads\hyderabad_cars.xlsx")
new_hyderabad_cars = column_processing(hyderabad_cars)
new_hyderabad_cars['city'] = 'Hyderabad'
new_hyderabad_cars.to_excel("new_hyderabad_cars.xlsx")

jaipur_cars = pd.read_excel(r"C:\Users\ASUS\Downloads\jaipur_cars.xlsx")
new_jaipur_cars = column_processing(jaipur_cars)
new_jaipur_cars['city'] = 'Jaipur'
new_jaipur_cars.to_excel("new_jaipur_cars.xlsx")

delhi_cars = pd.read_excel(r"C:\Users\ASUS\Downloads\delhi_cars.xlsx")
new_delhi_cars = column_processing(delhi_cars)
new_delhi_cars['city'] = 'Delhi'
new_delhi_cars.to_excel("new_delhi_cars.xlsx")

bangalore_cars = pd.read_excel(r"C:\Users\ASUS\Downloads\bangalore_cars.xlsx")
new_bangalore_cars = column_processing(bangalore_cars)
new_bangalore_cars['city'] = 'Bangalore'
new_bangalore_cars.to_excel("new_bangalore_cars.xlsx")

chennai_cars = pd.read_excel(r"C:\Users\ASUS\Downloads\chennai_cars.xlsx")
new_chennai_cars = column_processing(chennai_cars)
new_chennai_cars['city'] = 'Chennai'
new_chennai_cars.to_excel("chennai_cars_cars.xlsx")

dfs = [new_Kolkata_cars, new_hyderabad_cars, new_jaipur_cars, new_delhi_cars, new_bangalore_cars, new_chennai_cars]

concated_df = pd.concat(dfs,ignore_index=True)
concated_df.to_excel("concated_cars.xlsx",index=False)