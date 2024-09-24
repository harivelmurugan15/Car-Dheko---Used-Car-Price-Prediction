import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import GridSearchCV
import pickle

# Load the dataset
df = pd.read_excel(r"C:\Users\ASUS\IdeaProjects\Capstone project 3\Handeled_outliers.xlsx")
df.drop(['sta'], axis=1, inplace=True)
# Separate the features and the target
X = df.drop('price', axis=1)
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

feature_importances = rf.feature_importances_
importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=importance_df)
plt.title('Feature Importance from Random Forest Regressor')
plt.show()

# Select the top N features
top_features = importance_df.head(20)['Feature'].values
X_train_selected = X_train[top_features]
X_test_selected = X_test[top_features]

rf_selected = RandomForestRegressor(n_estimators=100, random_state=42)
rf_selected.fit(X_train_selected, y_train)
y_pred = rf_selected.predict(X_test_selected)

# Calculate and print the evaluation metric, e.g., R^2 score
r2_score1 = rf_selected.score(X_test_selected, y_test)
print(f"R^2 Score: {r2_score1}")

imp_fea = importance_df.head(20)['Feature'].values

X = df[imp_fea]
y = df['price']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=150)

param_grid = {
    'n_estimators': [100, 200, 300],  # Number of trees in the forest
    'max_depth': [10, 20, 30],  # Maximum depth of the tree
    'min_samples_split': [2, 5, 10],  # Minimum number of samples required to split an internal node
    'min_samples_leaf': [1, 2, 4],  # Minimum number of samples required to be at a leaf node
    'bootstrap': [True, False]  # Whether bootstrap samples are used when building trees
}

grid_search = GridSearchCV(estimator=model, param_grid=param_grid,
                           cv=5, n_jobs=-1, verbose=2, scoring='r2')

# Perform the grid search on the training data
grid_search.fit(x_train, y_train)

# Best parameters found by Grid Search
best_params = grid_search.best_params_
print("Best Hyperparameters:", best_params)

# Best model
best_model = grid_search.best_estimator_

print(best_model)

y_pred = best_model.predict(x_test)

# Evaluate performance
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"R2 Score: {r2:.3f}")
print(f"Mean Squared Error: {mse:.3f}")

input1 = []
input2 = []

for i in x_test.iloc[0].values:
    input1.append(i)
for i in x_test.iloc[1].values:
    input2.append(i)

new_data = [input1,input2]

y_pred = best_model.predict(new_data)

print("Predicted Output:", y_pred)

with open('best_model.pkl', 'wb') as file:
    pickle.dump(best_model, file)
