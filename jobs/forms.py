from django import forms
from jobs.models import MyUser,CompanyProfile,Jobs,JobSeekerProfile,Application
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    # password1 = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"})),
    # password2 = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"})),
    class Meta:
        model=MyUser
        fields=["email","role","password1","password2"]
        widgets={
            "email":forms.TextInput(attrs={"class":"form-control"}),
            "role": forms.Select(attrs={"class": "form-select"}),


        }


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
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"})

        }


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
        fields=["post_name","experience","description","end_date"]
        widgets={
            "post_name":forms.TextInput(attrs={"class":"form-control"}),
            "experience": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "end_date":forms.DateInput(attrs={"type":"date"})

        }



class AddJobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model=JobSeekerProfile
        fields=["name","qualification","experience","resume","photo"]
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "qualification": forms.TextInput(attrs={"class": "form-control"}),
            "experience": forms.TextInput(attrs={"class": "form-control"}),
            "resume": forms.FileInput(),


        }



class EditCompanyForm(forms.ModelForm):

    class Meta:
        model=CompanyProfile
        fields=["company_name","description","logo"]
        widgets={
            "company_name":forms.TextInput(attrs={"class":"form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"})

        }



class ApplicationForm(forms.ModelForm):

    class Meta:
        model=Application
        fields=["job","status","post_name","company"]
        widgets={
            "job":forms.TextInput(attrs={"class":"form-control","readonly":True}),
            "status":forms.TextInput(attrs={"class":"form-control","readonly":True}),
            "post_name":forms.TextInput(attrs={"class":"form-control","readonly":True}),
            "company": forms.TextInput(attrs={"class": "form-control", "readonly": True}),

        }
class EditApplicationForm(forms.ModelForm):

        class Meta:
            model = Application
            fields = ["status"]
            widgets = {
                "status": forms.Select(attrs={"class": "form-control"})
            }

