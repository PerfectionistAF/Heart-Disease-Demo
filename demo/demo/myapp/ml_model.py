"""""""""""""""""""""
Please note this is for reference ONLY, not for use in myapp
"""""""""""""""""""""

import numpy as np
import pandas as pd
import lightgbm as lgb
from pycaret.classification import *

# TODO dummy inputs
# Prompt the user to input the dataset as comma-separated values for each row
print("Enter the dataset as comma-separated values for each row. Press Enter after each row. Press Enter twice to finish.")
# Initialize an empty list to store rows
rows = []
# Continue accepting input until the user presses Enter twice
while True:
    row_input = input("Enter comma-separated values for a row (press Enter twice to finish): ")
    """
    age
    sex
    cp
    trestbps
    chol
    fbs
    restecg 
    thalach
    exang
    oldpeak
    slope
    ca
    thal
    """
    """
63 1 1 145 233 1 2 150 0 2.3 3 0.0 6.0
67 1 4 160 286 0 2 108 1 1.5 2 3.0 3.0
67 1 4 120 229 0 2 129 1 2.6 2 2.0 7.0
37 1 3 130 250 0 0 187 0 3.5 3 0.0 3.0
41 0 2 130 204 0 2 172 0 1.4 1 0.0 3.0
     """
    # If the user presses Enter without entering any values, break the loop
    if not row_input.strip():
        break
    # Split the input into individual values
    values = row_input.split(' ')
    # Ensure that exactly 13 values are provided
    if len(values) != 13:
        print("Error: You must provide exactly 13 values for each row.")
    else:
        converted_values = [int(float(value)) if float(value).is_integer() else float(value) for value in values if value.isdigit() or value.replace('.', '', 1).isdigit()]
        # Append the values to the list of rows
        rows.append(converted_values)
# Define column names
columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
# Create a pandas DataFrame from the list of rows with specified column names
df = pd.DataFrame(rows, columns=columns)
# Print the DataFrame
print("\nDataFrame created from user input:")
print(df)


# # TODO preprocessing
combined_df = df.copy()
combined_df['total_risk'] = combined_df['trestbps'] + combined_df['chol']
threshold_heart_rate = 150
print(combined_df.dtypes)
combined_df['exercise_angina'] = (combined_df['exang'] == 1) & (combined_df['thalach'] > threshold_heart_rate)
combined_df['cholesterol_hdl_ratio'] = combined_df['chol'] / combined_df['thalach']
# combined_df['num'] = combined_df['num'].apply(lambda x: 1 if x >= 0.5 else 0)
data = combined_df
print(data)



# #TODO load model
# from pycaret import *
pipeline = load_model('demo/my_best_pipeline')
# print pipeline
print(pipeline)



# #TODO predict
# copy data and remove target variable
data_unseen = data.copy()
# data_unseen.drop('num', axis = 1, inplace = True)
predictions = predict_model(pipeline, data = data_unseen)
print(predictions)


"""
https://archive.ics.uci.edu/dataset/45/heart+disease

Only 14 attributes used:
      1. #3  (age)       
      2. #4  (sex)       
      3. #9  (cp)        
      4. #10 (trestbps)  
      5. #12 (chol)      
      6. #16 (fbs)       
      7. #19 (restecg)   
      8. #32 (thalach)   
      9. #38 (exang)     
      10. #40 (oldpeak)   
      11. #41 (slope)     
      12. #44 (ca)        
      13. #51 (thal)      
      14. #58 (num)       (the predicted attribute)

63 1 1 145 233 1 2 150 0 2.3 3 0.0 6.0
        age:63
        sex: male
        cp: typical angina
        trestbps: 145
        chol: 233
        fbs: true
        restecg: showing probable or definite left ventricular hypertrophy by Estes' criteria
        thalach: 150 
        exang: no
        oldpeak: 2.3 
        slope: downsloping 
        ca: 0.0 
        thal: fixed defect
67 1 4 160 286 0 2 108 1 1.5 2 3.0 3.0
        age:67
        sex: male
        cp: asymptomatic
        trestbps: 160
        chol: 286
        fbs: false
        restecg: showing probable or definite left ventricular hypertrophy by Estes' criteria
        thalach: 108 
        exang: no
        oldpeak: 1.5
        slope: flat 
        ca: 3.0 
        thal: normal
67 1 4 120 229 0 2 129 1 2.6 2 2.0 7.0
        age:67
        sex: male
        cp: asymptomatic
        trestbps: 120
        chol: 229
        fbs: false
        restecg: showing probable or definite left ventricular hypertrophy by Estes' criteria
        thalach: 129 
        exang: yes
        oldpeak: 2.6
        slope: flat 
        ca: 3.0 
        thal: reversible defect
37 1 3 130 250 0 0 187 0 3.5 3 0.0 3.0
        age:37
        sex: male
        cp: non-anginal
        trestbps: 130
        chol: 250
        fbs: false
        restecg: normal
        thalach: 129 
        exang: yes
        oldpeak: 2.6
        slope: downsloping 
        ca: 0.0 
        thal: normal
41 0 2 130 204 0 2 172 0 1.4 1 0.0 3.0
        age:41
        sex: female
        cp: atypical anginal
        trestbps: 130
        chol: 204
        fbs: false
        restecg: showing probable or definite left ventricular hypertrophy by Estes' criteria
        thalach: 172 
        exang: no
        oldpeak: 1.4
        slope: upsloping 
        ca: 0.0 
        thal: normal

age: age in years
sex: sex (1 = male; 0 = female)
cp: chest pain type
        -- Value 1: typical angina
        -- Value 2: atypical angina
        -- Value 3: non-anginal pain
        -- Value 4: asymptomatic
trestbps: resting blood pressure (in mm Hg on admission to the hospital)
chol: serum cholestoral in mg/dl
fbs: (fasting blood sugar > 120 mg/dl)  (1 = true; 0 = false)
restecg: resting electrocardiographic results
        -- Value 0: normal
        -- Value 1: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV)
        -- Value 2: showing probable or definite left ventricular hypertrophy by Estes' criteria
thalach: maximum heart rate achieved
exang: exercise induced angina (1 = yes; 0 = no)
oldpeak = ST depression induced by exercise relative to rest
slope: the slope of the peak exercise ST segment
        -- Value 1: upsloping
        -- Value 2: flat
        -- Value 3: downsloping
ca: number of major vessels (0-3) colored by flourosopy
thal: 3 = normal; 6 = fixed defect; 7 = reversable defect
TARGET num: diagnosis of heart disease (angiographic disease status)
        -- Value 0: < 50% diameter narrowing
        -- Value 1: > 50% diameter narrowing
        (in any major vessel: attributes 59 through 68 are vessels)
"""