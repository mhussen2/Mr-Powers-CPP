# Part 1: Data Overview and Preparation

import kagglehub
import shutil
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score

source = kagglehub.dataset_download("adilshamim8/student-depression-dataset")
shutil.move(source, "./Lab_11_dataset")

file_path = "./Lab_11_dataset/student_depression_dataset.csv"
data = pd.read_csv(file_path)

print(data.info())
print(data.head())

print(data.isnull().sum())

if 'id' in data.columns:
    data = data.drop(columns=['id'])

sleep_map = {
    "Less than 5 hours": 4,
    "5-6 hours": 5.5,
    "7-8 hours": 7.5,
    "More than 8 hours": 9
}
data['Sleep Duration'] = data['Sleep Duration'].astype(str).str.replace("'", "")
data['Sleep Duration'] = data['Sleep Duration'].map(sleep_map)

binary_columns = ['Have you ever had suicidal thoughts ?', 'Financial Stress', 'Family History of Mental Illness']
for bcol in binary_columns:
    data[bcol] = data[bcol].map({'Yes': 1, 'No': 0})

categoricals = ['Gender', 'City', 'Profession', 'Dietary Habits', 'Degree']
lab = LabelEncoder()
for cat in categoricals:
    data[cat] = lab.fit_transform(data[cat])

simp = SimpleImputer(strategy='mean')
data[data.columns] = simp.fit_transform(data)

sns.histplot(data=data, x='Age')
plt.title('Distribution of Age')
plt.show()

sns.countplot(data=data, x='Gender', hue='Depression')
plt.title('Depression Cases by Gender')
plt.show()

plt.figure(figsize=(14,10))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

sns.boxplot(data=data, x='Depression', y='CGPA')
plt.title('CGPA vs Depression')
plt.show()

sns.pairplot(data[["Age", "CGPA", "Work/Study Hours", "Depression"]], hue="Depression")
plt.show()

# Part 2: Model Development and Evaluation

features = data.drop(columns='Depression')
target = data['Depression']

to_test = ['CGPA', 'Work Pressure', 'Job Satisfaction', 'Financial Stress', 'Dietary Habits']

for col in to_test:
    modified = features.drop(columns=[col])
    X_train, X_test, y_train, y_test = train_test_split(modified, target, test_size=0.2, random_state=1)
    tree = DecisionTreeRegressor(random_state=1)
    tree.fit(X_train, y_train)
    y_pred = tree.predict(X_test)
    print(f"\nOmitting: {col}")
    print("R2:", round(r2_score(y_test, y_pred), 4))
    print("MAE:", round(mean_absolute_error(y_test, y_pred), 4))

test_sizes = [0.1, 0.2, 0.3, 0.4]
for tsize in test_sizes:
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=tsize, random_state=1)
    tree = DecisionTreeRegressor(random_state=1)
    tree.fit(X_train, y_train)
    y_pred = tree.predict(X_test)
    print(f"\nSplit: {int((1-tsize)*100)}% train, {int(tsize*100)}% test")
    print("R2:", round(r2_score(y_test, y_pred), 4))
    print("MAE:", round(mean_absolute_error(y_test, y_pred), 4))
