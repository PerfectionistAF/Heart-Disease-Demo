from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import Group
from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):

#     class Meta:
#         model = CustomUser
#         fields = ("username", "email")


# class CustomUserCreationForm(UserCreationForm):
#     is_doctor = forms.BooleanField(label='Are you a Doctor?', required=False)

#     class Meta:
#         model = CustomUser
#         fields = ("username", "email", "password1", "password2", "is_doctor")

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             user.save()
#             if self.cleaned_data['is_doctor']:
#                 user.groups.add(Group.objects.get(name='Doctor'))
#             else:
#                 user.groups.add(Group.objects.get(name='Patient'))
#         return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")




from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class LoginForm(AuthenticationForm):
    # email = forms.EmailField(
    #     label='Email',
    #     widget=forms.EmailInput(attrs={"class": "form-control"})
    # )
    # password = forms.CharField(
    #     label='Password',
    #     widget=forms.PasswordInput(attrs={"class": "form-control"})
    # )
    pass


class SignUpForm(UserCreationForm):
    is_doctor = forms.BooleanField(label='Are you a Doctor?', required=False)

    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # email = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "password1", "password2", "is_doctor")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if self.cleaned_data['is_doctor']:
                user.groups.add(Group.objects.get(name='Doctor'))
            else:
                user.groups.add(Group.objects.get(name='Patient'))
        return user




# forms.py
from django import forms
from .models import DoctorPatientFile 
from django.core.exceptions import ValidationError


class DoctorPatientFileForm(forms.ModelForm):

    class Meta:
        model = DoctorPatientFile
        exclude = ["doctor", "reference_number", "diagnosis", "prognosis"]
        help_texts = {
                # 'age': ('Here is some help'),            
        }
    # this function will be used for the validation
    def clean(self):
 
        # data from the form is fetched using super function
        super(DoctorPatientFileForm, self).clean()
         
        # extract the username and text field from the data
        age = self.cleaned_data.get('age')
        trestbps = self.cleaned_data.get('trestbps')
        thalach = self.cleaned_data.get('thalach')
        oldpeak = self.cleaned_data.get('oldpeak')
        ca = self.cleaned_data.get('ca')
        chol = self.cleaned_data.get('chol')

 
        # TODO check for special characters or alphabet instead of numbers.
        errors = []
        if not float(age).is_integer():
            errors.append(ValidationError('Age must be a numeric integer value.'))
        elif age < 0 or age > 150:
            errors.append(ValidationError('Age is out of range.'))


        if not float(trestbps).is_integer():
            errors.append(ValidationError('Resting bp must be a numeric integer value.'))
        elif trestbps < 0 or trestbps > 300:
            errors.append(ValidationError('Resting bp is out of range.'))


        if not float(thalach).is_integer():
            errors.append(ValidationError('Maximum heart rate must be a numeric integer value.'))
        elif thalach < 0 or thalach > 300:
            errors.append(ValidationError('Maximum heart rate out of range.'))
        
        
        if not isinstance(oldpeak, (int, float)):
            errors.append(ValidationError('ST depression must be a numeric value.'))
        elif oldpeak < -10 or oldpeak > 10:
            errors.append(ValidationError('ST depression out of range.'))


        if not isinstance(ca, (int, float)):
            errors.append(ValidationError('Number of major vessels colored by fluoroscopy must be a numeric value.'))
        elif ca < 0 or ca > 3:
            errors.append(ValidationError('Number of major vessels colored by fluoroscopy out of range.'))
        
        
        if not isinstance(chol, (int, float)):
            errors.append(ValidationError("Serum cholesterol must be a numeric value."))
        elif chol < 0 or chol > 1000:
            errors.append(ValidationError('Total serum cholesterol out of range.'))

        # return any errors if found
        if errors:
            raise ValidationError(errors)
        
