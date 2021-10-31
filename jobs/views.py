from django.shortcuts import render,redirect
from jobs.models import MyUser,CompanyProfile,Jobs,JobSeekerProfile
from jobs.forms import RegistrationForm,SignInForm,AddCompanyForm,AddJobForm,AddJobSeekerProfileForm
from django.views.generic import CreateView,TemplateView,ListView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# users
# hari@gmail.com password@123 employer

# manu@gmail.com django@123 jobseeker


class RegistrationView(CreateView):
    model = MyUser
    form_class = RegistrationForm
    template_name = "jobs/registration.html"
    success_url = reverse_lazy("signin")

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["form"]=self.form_class
        return context


class SignInView(TemplateView):

    form_class = SignInForm
    template_name = "jobs/signin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        return context

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            user=authenticate(username=email,password=password)
            print(user)
            print("hello")

            if user:
                if user.role == "jobseeker":
                   login(request,user)
                   return redirect("jobseekerhome")

                else:
                   login(request,user)
                   return redirect("employerhome")

            else:
                print("failed")
                return redirect('signin')


class SignOutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("signin")


class EmployerHome(TemplateView):
    template_name = "jobs/employerhome.html"


class JobSeekerHomeView(TemplateView):
    template_name = "jobs/jobseekerhome.html"


class AddCompanyView(CreateView):
    model = CompanyProfile
    form_class = AddCompanyForm
    template_name = "jobs/addcompany.html"
    success_url = reverse_lazy("addcompany")

    def get(self,request,*args,**kwargs):
        form=self.form_class(request.user)
        return render(request,self.template_name,{"form":form})

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.user,request.POST,request.FILES)
        if form.is_valid():
            company=form.save(commit=False)
            company.user=request.user
            company.save()
            # print("company added")
            return redirect("addcompany")
        else:
            return render(request,self.template_name,{"form":form})



class AddJobView(CreateView):
    model = Jobs
    form_class = AddJobForm
    template_name = "jobs/addjob.html"


    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            job=form.save(commit=False)
            comp= CompanyProfile.objects.get(user_id=request.user.id)
            job.company=comp
            job.save()
            messages.success(request,"job posted successfully")
            return redirect("addjob")
        else:
            return render(request,self.template_name,{"form":form})

class ListJobView(ListView):
    model=Jobs
    template_name = 'jobs/listjob.html'
    context_object_name = "jobs"
    def get_queryset(self):
        comp = CompanyProfile.objects.get(user_id=self.request.user.id)
        queryset=self.model.objects.filter(company_id=comp.id)
        return queryset

class EditJobView(UpdateView):
    model=Jobs
    form_class = AddJobForm
    template_name = "jobs/editjob.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("listjob")



class AddJobSeekerProfileView(CreateView):
    model=JobSeekerProfile
    form_class = AddJobSeekerProfileForm
    template_name = "jobs/addjobseekerprofile.html"
    # success_url = reverse_lazy("addjobseekerprofile")

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST,request.FILES)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect("addjobseekerprofile")

        else:
            return render(request,self.template_name,{"form":form})


class ViewJobSeekerProfileVIew(ListView):
    model=JobSeekerProfile
    template_name = "jobs/viewjobseekerprofile.html"
    context_object_name = "profile"

    def get_queryset(self):
        queryset=JobSeekerProfile.objects.filter(user_id=self.request.user.id)
        return queryset





