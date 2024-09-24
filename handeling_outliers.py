import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel("Transformed_data.xlsx")

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
