# -*- coding: utf-8 -*-
"""Time Series Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yZgFGQYCe4Gc70wO6w_g6DYOX1Ur4bV8

# **Stock Market Prediction using Python**

by Jay Gohil

---

# **Installing and importing necessary libraries**

---
"""

#Installing 'quandl'
!pip install quandl

#Impoting necessary packages and libraries
import quandl, math
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

"""# **Taking data of stock from 'quandl'**

---
"""

#Defining the API key for Qyandl
auth_tok = "zT6DNLxAdJuUdyySgxGN"

#Taking the data from Quandle into variable 'data'
data = quandl.get("EOD/AAPL", trim_start = "2000-12-12", trim_end = "2020-12-30", authtoken=auth_tok)

#Printing the dataset
print(data)

"""# **Engineering the data**

---
"""

#Taking only necessary columns in dataset (for creating new columns)
data = data[['Adj_Open',  'Adj_High',  'Adj_Low',  'Adj_Close', 'Adj_Volume']]

#Creating new columns, and adding data for them using specific formula
data['HL_PCT'] = (data['Adj_High'] - data['Adj_Low']) / data['Adj_Close'] * 100.0
data['PCT_change'] = (data['Adj_Close'] - data['Adj_Open']) / data['Adj_Open'] * 100.0

#Taking only ncessary columns in final working dataset
data = data[['Adj_Close', 'HL_PCT', 'PCT_change', 'Adj_Volume']]

#Printing the updated dataset
print(data)

"""# **Visualizing the dataset**

---
"""

print(data["Adj_Close"].plot())

print(data["Adj_Volume"].plot())

print(data["PCT_change"].plot())

print(data["HL_PCT"].plot())

#Checking correlation among features
print("Visualizing correlation between features using heatmap -->\n")
sns.heatmap(data.corr(method='pearson'), cmap='Blues')

"""# **Cleaning and preparing dataset for Machine Learning**

---
"""

#Defining forecasting column
forecast_col = 'Adj_Close'

#Replacing NaN values with '-99999' value which is considered as an outlier by most ML classifiers
data.fillna(value=-99999, inplace=True)

#Forecasting out 1% of the dataset's length
forecast_out = int(math.ceil(0.01 * len(data)))

#Adding a new coumn for 'label'
data['label'] = data[forecast_col].shift(-forecast_out)

print(data)

#Preparing X and y
X = np.array(data.drop(['label'], 1))
X = preprocessing.scale(X)
X = X[:-forecast_out]
data.dropna(inplace=True) #Dropping NaN values
y = np.array(data['label'])

#Splitting the data into 80:20 ratio
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#Training the linear regression model
clf = LinearRegression(n_jobs=-1)
clf.fit(X_train, y_train)

#Predicting y values
y_predicted = clf.predict(X_test)

#Printing predicted values
print(y_predicted)

temp1 = []
temp2 = []
temp3 = []

for i in range(20):
  temp1.append(int(y_test[i]))

for i in range(20):
  temp2.append(int(y_predicted[i]))


for i in range(20):
  temp3.append(i)

#Printing original values
print("Actual values -->")
print(temp1)

#Printing predicted values
print("\nPredicted values -->")
print(temp2)

print("\n"*2)

plt.scatter(temp3, temp1, marker="*", color = 'blue')
plt.scatter(temp3, temp2, color = 'orange')

#Finding MSE value
MSE = mean_squared_error(y_test, y_predicted)
print("Mean Squared Error: %.5f" %MSE)

# Finding confidence value
confidence = clf.score(X_test, y_predicted)
print("Confidence:         %.5f" %confidence)

#Making prediction on custom value
custom_pred = clf.predict([[-2.93777787e-01, -9.02387310e-01, -1.05003377e-01, -3.19550752e-01]])
print("The prediction for custom values : %.5f" % custom_pred)

"""# **Thank you.**

---
"""
