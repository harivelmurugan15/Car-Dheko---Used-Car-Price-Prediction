import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import pickle

def value_vectorizer(df1):
    vectorizer = CountVectorizer()
    encoded_features = vectorizer.fit_transform(df1).toarray()

    kmeans = KMeans(n_clusters=3, random_state=42)  # Example: 3 clusters
    clusters = kmeans.fit_predict(encoded_features)

    df['Cluster'] = clusters
    df1 = df['Cluster']
    return df1


df = pd.read_excel(r"concated_cars.xlsx")


df['Kms Driven'] = [str(i).split()[0] for i in df['Kms Driven']]
df['Kms Driven'] = df['Kms Driven'].str.replace(',', '').astype(float)
df['price'] = [i.split()[1] for i in df['price']]
df['price'] = df['price'].str.replace(',', '').astype(float)
df['Engine Displacement'] = [str(i).split()[0] for i in df['Engine Displacement']]
df['Mileage'] = [str(i).split()[0] for i in df['Mileage']]

for i in df['price']:
    if i > 1000:
        i1 = i / 100000
        df['price'].replace(i, i1, inplace=True)

for i in df['Max Power']:
    if len(str(i)) > 10:
        df['Max Power'].replace(i, np.nan, inplace=True)
    i1 = ''.join([char for char in str(i) if char.isdigit() or char == '.'])
    df['Max Power'].replace(i, i1, inplace=True)

for i in df['Torque']:
    i1 = ''.join([char for char in str(i) if char.isdigit() or char == '.'])
    df['Torque'].replace(i, i1, inplace=True)

for i in df['Miscellaneous_Gear Box']:
    i1 = ''.join([char for char in str(i) if char.isdigit() or char == '.'])
    if i1:
        i1=i1[0]
    df['Miscellaneous_Gear Box'].replace(i, i1, inplace=True)

for i in df['Miscellaneous_Drive Type']:
    if i == "AWD" or i == "4WD" or i == "4X4" or i == "Permanent all-wheel drive quattro":
        df['Miscellaneous_Drive Type'].replace(i, "Four Wheel Drive", inplace=True)
    else:
        df['Miscellaneous_Drive Type'].replace(i, "Two Wheel Drive", inplace=True)

for i in df['Miscellaneous_Cargo Volumn']:
    i1 = ''.join([char for char in str(i) if char.isdigit() or char == '.'])
    df['Miscellaneous_Cargo Volumn'].replace(i, i1, inplace=True)

for i in df['Miscellaneous_Top Speed']:
    i1 = ''.join([char for char in str(i) if char.isdigit() or char == '.'])
    df['Miscellaneous_Top Speed'].replace(i, i1, inplace=True)



df['Comfort & Convenience'] = value_vectorizer(df['Comfort & Convenience'])
df['Interior'] = value_vectorizer(df['Interior'])
df['Exterior'] = value_vectorizer(df['Exterior'])
df['Safety'] = value_vectorizer(df['Safety'])
df['Entertainment & Communication'].ffill(inplace=True)
df['Entertainment & Communication'] = value_vectorizer(df['Entertainment & Communication'])

model = LabelEncoder()
# Create a dictionary to store all the mappings
mappings = {}

# List of columns to encode
columns_to_encode = [
    'bt', 'oem', 'Year of Manufacture', 'model', 'Insurance Validity', 'Fuel Type',
    'Transmission', 'Max Power', 'Torque', 'Mileage', 'Engine Displacement',
    'Engine and Transmission_Value Configuration', 'Engine and Transmission_Fuel Suppy System',
    'Miscellaneous_Drive Type', 'Miscellaneous_Steering Type', 'Miscellaneous_Front Brake Type',
    'Miscellaneous_Rear Brake Type', 'Miscellaneous_Tyre Type', 'city'
]

# Create mappings and apply label encoding
for col in columns_to_encode:
    mappings[col] = dict(zip(df[col], model.fit_transform(df[col])))
    df[col] = model.transform(df[col])

mappings['Features'] = dict(zip(df['Features'], value_vectorizer(df['Features'])))
df['Features'] = value_vectorizer(df['Features'])

mappings.pop('Fuel Type')
mappings.pop('Engine and Transmission_Value Configuration')
mappings.pop('Miscellaneous_Drive Type')
mappings.pop('Miscellaneous_Steering Type')

for col, mapping in mappings.items():
    print(f"Mapping for {col}: {mapping}")

with open('mappings.pkl','wb') as file:
    pickle.dump(mappings,file)

# df['bt'] = model.fit_transform(df['bt'])
# df['oem'] = model.fit_transform(df['oem'])
# df['Year of Manufacture'] = model.fit_transform(df['Year of Manufacture'])
# df['model'] = model.fit_transform(df['model'])
# df['Insurance Validity'] = model.fit_transform(df['Insurance Validity'])
# df['Fuel Type'] = model.fit_transform(df['Fuel Type'])
# df['Transmission'] = model.fit_transform(df['Transmission'])
# df['Max Power'] = model.fit_transform(df['Max Power'])
# df['Torque'] = model.fit_transform(df['Torque'])
# df['Mileage'] = model.fit_transform(df['Mileage'])
# df['Engine Displacement'] = model.fit_transform(df['Engine Displacement'])
# df['Engine and Transmission_Value Configuration'] = model.fit_transform( df['Engine and Transmission_Value Configuration'])
# df['Engine and Transmission_Fuel Suppy System'] = model.fit_transform(df['Engine and Transmission_Fuel Suppy System'])
# df['Miscellaneous_Drive Type'] = model.fit_transform(df['Miscellaneous_Drive Type'])
# df['Miscellaneous_Steering Type'] = model.fit_transform(df['Miscellaneous_Steering Type'])
# df['Miscellaneous_Front Brake Type'] = model.fit_transform(df['Miscellaneous_Front Brake Type'])
# df['Miscellaneous_Rear Brake Type'] = model.fit_transform(df['Miscellaneous_Rear Brake Type'])
# df['Miscellaneous_Tyre Type'] = model.fit_transform(df['Miscellaneous_Tyre Type'])
# df['city'] = model.fit_transform(df['city'])
df.drop(['Cluster'], axis=1, inplace=True)

df.to_excel("Transformed_data.xlsx",index=False)
