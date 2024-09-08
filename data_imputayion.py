import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel("Transformed_data.xlsx")

df.drop(['Miscellaneous_Top Speed', 'Miscellaneous_Cargo Volumn'], axis=1, inplace=True)

# Mean imputaion for missing regression value

df['Kms Driven'] = df['Kms Driven'].fillna(df['Kms Driven'].mean())


# Mode imputation for the missing categorical data

df['Year of Manufacture'] = df['Year of Manufacture'].fillna(df['Year of Manufacture'].mode()[0])
df['Seats'] = df['Seats'].fillna(df['Seats'].mode()[0])
df['Miscellaneous_Gear Box'] = df['Miscellaneous_Gear Box'].fillna(df['Miscellaneous_Gear Box'].mode()[0])
df['Engine and Transmission_No of Cylinder'] = df['Engine and Transmission_No of Cylinder'].fillna(
    df['Engine and Transmission_No of Cylinder'].mode()[0])
df['Engine and Transmission_Values per Cylinder'] = df['Engine and Transmission_Values per Cylinder'].fillna(
    df['Engine and Transmission_Values per Cylinder'].mode()[0])
df['Miscellaneous_No Door Numbers'] = df['Miscellaneous_No Door Numbers'].fillna(
    df['Miscellaneous_No Door Numbers'].mode()[0])
df['Engine Displacement'] = df['Engine Displacement'].fillna(df['Engine Displacement'].mode()[0])
df['Mileage'] = df['Mileage'].fillna(df['Mileage'].mode()[0])
df['Max Power'] = df['Max Power'].fillna(df['Max Power'].mode()[0])
df['Torque'] = df['Torque'].fillna(df['Torque'].mode()[0])
sns.boxplot(df['price'])
plt.show()

df['price'] = df['price'].astype(float)
df['sta'] = (df['price'] - df['price'].mean()) / df['price'].std()
print("Number of rows before filtering:", len(df))
df = df[(df['sta'] > -2) & (df['sta'] < 2)]
print("Number of rows after filtering:", len(df))
sns.boxplot(df['price'])

df.drop(['sta'], axis=1, inplace=True)

sns.boxplot(df['Kms Driven'])
plt.show()

df['Kms Driven'] = df['Kms Driven'].astype(float)
df['sta'] = (df['Kms Driven'] - df['Kms Driven'].mean()) / df['Kms Driven'].std()
print("Number of rows before filtering:", len(df))
df = df[(df['Kms Driven'] > -2) & (df['sta'] < 2)]
print("Number of rows after filtering:", len(df))
sns.boxplot(df['Kms Driven'])

df.to_excel("Handeled_outliers.xlsx",index=False)
