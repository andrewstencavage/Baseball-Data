# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 05:10:58 2018

@author: anarayan
"""

import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  

from sklearn.model_selection import train_test_split
#new version of sklearn has train_test_split in model_selection library
#from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn import metrics  

#fill up a dataframe with data
dataset = pd.read_csv('petrol_consumption.csv')  
print(dataset.shape)
print(dataset.head())
print(dataset.describe())

#prepare the data
#create attributes and labels
#use column names for creating an attribute set and label
x = dataset[['Petrol_tax', 'Average_income', 'Paved_Highways',  
       'Population_Driver_licence(%)']]
y = dataset['Petrol_Consumption'] 
 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

regressor = LinearRegression()  
regressor.fit(x_train, y_train) 

#the regression model has to find the most optimal coefficients for all the attributes
coeff_df = pd.DataFrame(regressor.coef_, x.columns, columns=['Coefficient'])  
print(coeff_df)

y_pred = regressor.predict(x_test)  

df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})  
print(df)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

