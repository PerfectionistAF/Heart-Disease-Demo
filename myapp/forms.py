from django import forms

class CreateRefForm(forms.Form):
    age = forms.IntegerField(label='Age (years)')#, help_text='Enter age in years')
    sex = forms.ChoiceField(label='Sex', choices=[(1, 'Male'), (0, 'Female')], widget=forms.RadioSelect())#, help_text='Select gender')
    cp = forms.ChoiceField(label='Chest Pain Type', choices=[(1, 'Typical Angina'), (2, 'Atypical Angina'), (3, 'Non-Anginal Pain'), (4, 'Asymptomatic')])#, help_text='Select chest pain type')
    trestbps = forms.IntegerField(label='Resting Blood Pressure (mm Hg) on admission to the hospital')#, help_text='Enter resting blood pressure in mm Hg on admission to the hospital')
    chol = forms.IntegerField(label='Serum Cholesterol (mg/dl)')#, help_text='Enter serum cholesterol in mg/dl')
    fbs = forms.ChoiceField(label='Fasting Blood Sugar > 120 mg/dl?', choices=[(1, 'True'), (0, 'False')], widget=forms.RadioSelect()) #, help_text='Select fasting blood sugar level'
    restecg = forms.ChoiceField(label='Resting Electrocardiographic Results', choices=[(0, 'Normal'), (1, 'Abnormal - ST-T wave'), (2, 'Abnormal - Left Ventricular Hypertrophy')])#, help_text='Select resting electrocardiographic results')
    thalach = forms.IntegerField(label='Maximum Heart Rate Achieved')#, help_text='Enter maximum heart rate achieved')
    exang = forms.ChoiceField(label='Exercise Induced Angina?', choices=[(1, 'Yes'), (0, 'No')], widget=forms.RadioSelect()) #, help_text='Select exercise induced angina'
    oldpeak = forms.FloatField(label='ST Depression Induced by Exercise Relative to Rest')#, help_text='Enter ST depression induced by exercise relative to rest')
    slope = forms.ChoiceField(label='Slope of the Peak Exercise ST Segment', choices=[(1, 'Upsloping'), (2, 'Flat'), (3, 'Downsloping')])#, help_text='Select slope of the peak exercise ST segment')
    ca = forms.FloatField(label='Number of Major Vessels Colored by Fluoroscopy', help_text='Hint: Enter decimal number (between 0-3).')#, widget=forms.TextInput(attrs={'type': 'text'}))
    thal = forms.ChoiceField(label='Thalassemia', choices=[(3, 'Normal'), (6, 'Fixed Defect'), (7, 'Reversible Defect')])#, help_text='Select thalassemia type')