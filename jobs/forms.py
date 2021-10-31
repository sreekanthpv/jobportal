from django import forms
from jobs.models import MyUser,CompanyProfile,Jobs,JobSeekerProfile
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model=MyUser
        fields=["email","role"]

class SignInForm(forms.Form):
    email=forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class AddCompanyForm(forms.ModelForm):

    def __init__(self,user,*args,**kwargs):

        self.user=user

        print("user==========",user.id)
        super().__init__(*args,**kwargs)



    class Meta:
        model=CompanyProfile
        fields=["company_name","description","logo"]


    def clean(self):
        cleaned_data=super().clean()
        id=self.user.id
        profile=CompanyProfile.objects.filter(user_id=id)
        if profile:
            msg="cannot add more than 1 company"
            self.add_error("company_name",msg)

class AddJobForm(forms.ModelForm):
    class Meta:
        model=Jobs
        fields=["post_name","experience","description"]



class AddJobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model=JobSeekerProfile
        fields=["name","qualification","experience","resume"]

