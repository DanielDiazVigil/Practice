# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 17:46:52 2021

@author: Daniel
"""

import pandas as pd
import os 
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

os.chdir(r'C:\Users\Daniel\Desktop\Coding\Practice\Machine Learning Practice\RandomForrest\HeartDiseasePredictor')
print(os.getcwd())

#            Importing Heart CSV 

heart_data = pd.read_csv('heart.csv')
print(heart_data.head())

#           Creating Columns Separate Columns for Sex, Dropping Original Sex Column 
heart_data['Male'] = heart_data['Sex'].apply(lambda x: 1 if x == 'M' else 0)
heart_data['Female'] = heart_data['Sex'].apply(lambda x: 1 if x == 'F' else 0)

heart_data = heart_data.drop(['Sex'], axis = 'columns')

#            Getting Chest Pain Types 

chest_pain_types_list = []
for i in range(len(heart_data['ChestPainType'])):
               if heart_data['ChestPainType'][i] not in chest_pain_types_list:
                   chest_pain_types_list.append(heart_data['ChestPainType'][i])

#            Creating Column For Each Pain Type 1 == present 0 == not present, Droping ChestPainType Column
for pain_type in chest_pain_types_list:
    heart_data[pain_type] = heart_data['ChestPainType'].apply(lambda x: 1 if x == pain_type else 0)
                   
heart_data = heart_data.drop(['ChestPainType'], axis = 'columns') 
    
    
#       Getting Resting ECG Types 
resting_ecg_types = []
for i in range(len(heart_data['RestingECG'])):
    if heart_data['RestingECG'][i] not in resting_ecg_types:
        resting_ecg_types.append(heart_data['RestingECG'][i])
        
# Creating Separate Column For Each Resting ECG Type; Removing Previous RestingECG Column 

for ecg_type in resting_ecg_types:
    heart_data[ecg_type] = heart_data['RestingECG'].apply(lambda x: 1 if x == ecg_type else 0)

heart_data = heart_data.drop(['RestingECG'], axis = 'columns')



#  Converting ExerciseAngina Column from string categorical value to numerical categorical value

heart_data['ExerciseAngina'] = heart_data['ExerciseAngina'].apply(lambda x: 0 if x == 'N' else 1)
    




# List of ST Slope types 
st_slope_type = ['Up', 'Down', 'Flat']

# Creating Separate Column for Each ST Slope type Dropping Original ST_slope column

for st_type in st_slope_type:
    heart_data[st_type] = heart_data['ST_Slope'].apply(lambda x: 1 if x == st_type else 0)
    
heart_data = heart_data.drop(['ST_Slope'], axis = 'columns')

# Renaming Column Names to be more descriptive 
heart_data = heart_data.rename(columns = {
    'ATA': 'ATA_pain', 'NAP': 'NAP_Pain', 'ASY': 'ASY_Pain', 'TA': 'TA_Pain',
    'Normal': 'Normal_ECG', 'ST': 'ST_ECG', 'LVH': 'LVH_ECG', 'Up':'St_Slope_Up',
    'Down':'St_Slope_Down', 'Flat':'St_Slope_Flat'
    })



X_train, X_test, y_train, y_test = train_test_split(heart_data.drop(['HeartDisease'],
                                                                    axis="columns"),
                                                    heart_data.HeartDisease, test_size = 0.2)


# Creating Model 

heart_disease_model = RandomForestClassifier(n_estimators= 40)

heart_disease_model.fit(X_train, y_train)


print(heart_disease_model.score(X_test, y_test))




