from django.shortcuts import render, HttpResponse, redirect
from .forms import CreateRefForm
from .models import UserSubmission
# for my model prediction
import numpy as np
import pandas as pd
import lightgbm as lgb
from pycaret.classification import *
#for ref_num generation
from datetime import datetime
from django.contrib.gis.geoip2 import GeoIP2
import hashlib
# Create your views here.



def home(request):
    form = CreateRefForm()
    return render(request, "home.html", {'form': form})

def submission(request):
    return render(request, "submission.html")

def get_predictions(user_data): #user_data: dict
    # load saved model...
    # preprocess request.POST form data for model...
    # model predictions...

    # # TODO preprocessing
    row = [
        user_data['age'],
        user_data['sex'],
        user_data['cp'],
        user_data['trestbps'],
        user_data['chol'],
        user_data['fbs'],
        user_data['restecg'],
        user_data['thalach'],
        user_data['exang'],
        user_data['oldpeak'],
        user_data['slope'],
        user_data['ca'],
        user_data['thal']
        ]
    rows = []
    # Append the values to the list of rows
    rows.append(row)
    columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    # Create a pandas DataFrame from the list of rows with specified column names
    df = pd.DataFrame(rows, columns=columns)

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
    pipeline = load_model('my_best_pipeline')
    # print pipeline
    # print(pipeline)



    # #TODO predict
    # copy data and remove target variable
    data_unseen = data.copy()
    # data_unseen.drop('num', axis = 1, inplace = True)
    predictions = predict_model(pipeline, data = data_unseen)
    print(predictions)
    return predictions


def result(request):
    if request.method == 'POST':
        form = CreateRefForm(request.POST)
        if (form.is_valid()):
            user_output = get_predictions(form.cleaned_data) #returns dataframe of user input with prediction_label and predictions_score
            # generate ref_num = 'PT67-0-240306-EG-12345678'
            ref_num = "PT" + str(user_output['age'][0]) + '-' + str(user_output['prediction_label'][0]) + "-"

            current_date = datetime.now().strftime('%y%m%d')
            ref_num = ref_num + current_date + '-'
            
            # g = GeoIP2() #TODO this code should work
            # remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
            # if remote_addr:
            #     address = remote_addr.split(',')[-1].strip()
            # else:
            #     address = request.META.get('REMOTE_ADDR')
            # current_location = g.country_code(address)
            current_location = 'EG'
            ref_num = ref_num + current_location + '-'
           
            checksum = hashlib.sha256(ref_num.encode()).hexdigest()  # Calculate the SHA-256 hash of the data
            checksum_short = checksum[:8] # Take the first 8 characters of the hash as the checksum
            ref_num = ref_num + checksum_short
            

            if int(user_output['prediction_label']) == 0:
                diag = "< 50% diameter narrowing"
            else:
                diag = "> 50% diameter narrowing"
            user_submission = UserSubmission.objects.create(reference_number=ref_num, diagnosis=diag)
            user_submission.save()
            return render(request, "result.html", {"ref_num" : user_submission.reference_number})
            # combined_row = '  '.join(str(value) for value in user_output.iloc[0])
            # return HttpResponse('New user submission: ' +  combined_row
            #                     + "    reference number: " + user_submission.reference_number + " diagnosis: " + user_submission.diagnosis 
            #                     + "     with prediction_score: " + user_output['prediction_score'])
    
    else:
        return redirect('home')