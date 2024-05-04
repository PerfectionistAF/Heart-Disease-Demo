from django.shortcuts import render, HttpResponse, redirect
from .forms import DoctorPatientFileForm
from .models import DoctorPatientFile, CustomUser
# for my model prediction
import numpy as np
import pandas as pd
import lightgbm as lgb
from pycaret.classification import *
# for ref_num generation
from datetime import datetime
from django.contrib.gis.geoip2 import GeoIP2
import hashlib
# for SignUpView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group




# class SignUpView(CreateView): #class-based views
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"

def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('home')
        #     else:
        #         msg= 'invalid credentials'
        # else:
        #     msg = 'error validating form'
    return render(request, 'registration/login.html', {'form': form})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['is_doctor']:
                user.groups.add(Group.objects.get(name='Doctor'))
            else:
                user.groups.add(Group.objects.get(name='Patient'))
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def home(request):
    if request.method == 'POST':
        form = DoctorPatientFileForm(request.POST)
        if form.is_valid():
            # Process form data
            user_output = get_predictions(form.cleaned_data) #returns dataframe of user input with prediction_label and predictions_score

            if int(user_output['prediction_label']) == 0:
                diag = "MI"
            else:
                diag = "not MI"

            
            first_row_values = user_output.iloc[0].astype(str)
            joined_string = "-".join(first_row_values)
            ref_num = "PT" + joined_string \
                + "-" + datetime.now().strftime('%y/%m/%d, %H:%M:%S') \
                + "-" + "EG" + "-"

            checksum = hashlib.sha256(ref_num.encode()).hexdigest()  # Calculate the SHA-256 hash of the data
            checksum_short = checksum[:32] # Take the first 32 characters of the hash as the checksum
            ref_num = "PT-" + checksum_short

            # user_submission = DoctorPatientFile.objects.create(reference_number=ref_num, diagnosis=diag)
            # user_submission.save()


# data=request.POST
#             username=data.get("user_name")
#             email=data.get("email")
#             password=data.get("password")
            # user=User.objects.create_user(username, email, password)
#             group=Group.objects.get(name='studio')
#             group.user_set.add(user)
#             studio_form.user_id=user.id
            doctor_patient_file = form.save(commit=False)  # Don't save to database yet
            doctor_patient_file.doctor = request.user  # Assuming 'doctor' is the ForeignKey field to the User model


            doctor_patient_file.reference_number = ref_num
            doctor_patient_file.diagnosis = diag
            doctor_patient_file.prognosis = diag

            # # Assuming you have a variable 'patient_email' containing the patient's unique email address
            # patient_email = "salma@example.com"  # Replace this with the actual email
            # # Check if a user with the given email exists
            # try:
            #     patient_user = CustomUser.objects.get(email=patient_email)
            # except CustomUser.DoesNotExist:
            #     # Handle the case where the user with the given email doesn't exist
            #     # You can raise an exception, redirect the user, or handle it as per your application's logic
            #     pass
            # else:
            #     doctor_patient_file.patient = patient_user
            
    
            
            doctor_patient_file.save()

            query_results = DoctorPatientFile.objects.filter(doctor=request.user)
            return render(request, "results.html", {'new_file_added': True, 'reference_number': ref_num, 'query_results': query_results})
    else:
        form = DoctorPatientFileForm()
    return render(request, 'home.html', {'model_form': form})


# age:63
# sex: male
# cp: typical angina
# trestbps: 145
# chol: 233
# fbs: true
# restecg: showing probable or definite left ventricular hypertrophy by Estes' criteria
# thalach: 150 
# exang: no
# oldpeak: 2.3 
# slope: downsloping 
# ca: 0.0 
# thal: fixed defect



def submission(request):
    """ search function  """
    if request.method == "POST":
        query_name = request.POST.get('search', None)
        if query_name:
            results = DoctorPatientFile.objects.filter(reference_number=query_name)
            return render(request, 'submission.html', {"results":results})

    return render(request, 'submission.html')


def results_table(request):
    query_results = DoctorPatientFile.objects.filter(doctor=request.user)
    return render(request, "results.html", {'query_results': query_results})

def get_predictions(user_data): #user_data: dict
    # load saved model...
    # preprocess request.POST form data for model...
    # model predictions...

    # preprocessing
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



    # load model
    pipeline = load_model('my_best_pipeline')
    # print pipeline
    # print(pipeline)



    # predict
    # copy data and remove target variable
    data_unseen = data.copy()
    # data_unseen.drop('num', axis = 1, inplace = True)
    predictions = predict_model(pipeline, data = data_unseen)
    print(predictions)
    return predictions

