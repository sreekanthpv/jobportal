from django.shortcuts import render,redirect
from jobs.models import MyUser,CompanyProfile,Jobs,JobSeekerProfile,Application
from jobs.forms import RegistrationForm,SignInForm,AddCompanyForm,AddJobForm,AddJobSeekerProfileForm,EditCompanyForm,ApplicationForm,EditApplicationForm
from django.views.generic import CreateView,TemplateView,ListView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from jobs.decorators import signin_required,employer_signin,jobseeker_signin
from jobs.filters import JobFilter
from django_filters.views import FilterView
# users
# hari@gmail.com django@123 employer
# sreekanth@

# jobseeker  sarath@,django,
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

#
@method_decorator(signin_required,name="dispatch")
@method_decorator(employer_signin,name='dispatch')
class EmployerHome(TemplateView):
    template_name = "jobs/employerhome.html"


@method_decorator(signin_required,name="dispatch")
@method_decorator(jobseeker_signin,name='dispatch')
class JobSeekerHomeView(ListView):
    model = Jobs
    template_name = "jobs/jobseekerhome.html"
    context_object_name = "jobs"

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset


#
@method_decorator(signin_required,name="dispatch")
@method_decorator(employer_signin,name='dispatch')
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
            return redirect("viewcompanyprofile")
        else:
            return render(request,self.template_name,{"form":form})


#
@method_decorator(signin_required,name="dispatch")
@method_decorator(employer_signin,name='dispatch')
class ViewCompanyProfileView(ListView):
    model=CompanyProfile
    template_name = "jobs/viewcompanyprofile.html"
    context_object_name = "company"

    def get_queryset(self):
        queryset=CompanyProfile.objects.filter(user_id=self.request.user.id)
        return queryset


@method_decorator(signin_required,name="dispatch")
@method_decorator(employer_signin,name='dispatch')
class EditCompanyProfileView(UpdateView):
    model=CompanyProfile
    form_class = EditCompanyForm
    template_name = "jobs/addcompany.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("viewcompanyprofile")
    # def get(self, request, *args, **kwargs):
    #
    #     company = CompanyProfile.objects.get(user_id=request.user.id)
    #     form = self.form_class(instance=company)
    #     return render(request, self.template_name, {"form": form})
    #
    # def post(self, request, *args, **kwargs):
    #     company = CompanyProfile.objects.get(user_id=request.user.id)
    #     form = self.form_class( request.POST, request.FILES,instance=company)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("viewcompanyprofile")
    #     else:
    #         return render(request, self.template_name, {"form": form})


#
@method_decorator(signin_required,name="dispatch")
@method_decorator(employer_signin,name='dispatch')
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
            return redirect("listjob")
        else:
            return render(request,self.template_name,{"form":form})


@method_decorator(signin_required,name="dispatch")
@method_decorator(employer_signin,name='dispatch')
class ListJobView(ListView):
    model=Jobs
    template_name = 'jobs/listjob.html'
    context_object_name = "jobs"
    def get_queryset(self):
        comp = CompanyProfile.objects.get(user_id=self.request.user.id)
        queryset=self.model.objects.filter(company_id=comp.id)
        return queryset


@method_decorator(signin_required,name="dispatch")
@method_decorator(employer_signin,name='dispatch')
class EditJobView(UpdateView):
    model=Jobs
    form_class = AddJobForm
    template_name = "jobs/editjob.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("listjob")

class DeleteJobs(DeleteView):
    model = Jobs
    template_name = "jobs/employerdeleteapplication.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("listjob")




@method_decorator(signin_required,name="dispatch")
@method_decorator(jobseeker_signin,name='dispatch')
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
            return redirect("viewjobseekerprofile")

        else:
            return render(request,self.template_name,{"form":form})



@method_decorator(signin_required,name="dispatch")
@method_decorator(jobseeker_signin,name='dispatch')
class ViewJobSeekerProfileVIew(ListView):
    model=JobSeekerProfile
    template_name = "jobs/viewjobseekerprofile.html"
    context_object_name = "profile"

    def get_queryset(self):
        queryset=JobSeekerProfile.objects.filter(user_id=self.request.user.id)
        return queryset



@method_decorator(signin_required,name="dispatch")
@method_decorator(jobseeker_signin,name='dispatch')
class EditJobSeekerProfileView(UpdateView):
    model = JobSeekerProfile
    form_class = AddJobSeekerProfileForm
    template_name = "jobs/addjobseekerprofile.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("viewjobseekerprofile")



@method_decorator(signin_required,name="dispatch")
@method_decorator(jobseeker_signin,name='dispatch')
class JobseekerApplicationView(CreateView):
    model = Jobs
    form_class = ApplicationForm
    template_name = "jobs/application.html"
    # context_object_name = "jobs"
    pk_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        job=self.model.objects.get(id=kwargs["id"])
        post=job.post_name
        company=CompanyProfile.objects.get(id=job.company_id)
        # print("post======",post)
        form=self.form_class(initial={"job":job,"post_name":post,"company":company})
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            # id=form.cleaned_data["job"]
            # status=form.cleaned_data["status"]
            app=form.save(commit=False)
            app.user=request.user
            app.email=request.user
            app.save()
            return redirect("listapplication")
        else:
            return render(request,self.template_name,{"form":form})


@method_decorator(signin_required,name="dispatch")
@method_decorator(jobseeker_signin,name='dispatch')
class ListApplicationView(ListView):
    model=Application
    template_name = "jobs/listapplication.html"
    context_object_name = "application"

    def get_queryset(self):
        queryset=self.model.objects.filter(user_id=self.request.user.id)
        return queryset


class JobSearch(FilterView):
    model=Jobs
    filterset_class = JobFilter
    template_name = "jobs/jobsearch.html"
    # context_object_name = "fil"

    def get_queryset(self):
        queryset=Jobs.objects.all()
        return queryset





@method_decorator(signin_required,name="dispatch")
@method_decorator(employer_signin,name='dispatch')
class EmployerListApplication(ListView):
    model=Application
    template_name = "jobs/employerlistapplication.html"
    context_object_name = "application"

    def get_queryset(self):
        user=self.request.user
        # print("user=============",user.id)
        company=CompanyProfile.objects.get(user_id=user.id)
        # print("company===",company.id)
        # job=Jobs.objects.get(company_id=company)
        queryset=self.model.objects.filter(company_id=company.id)
        return queryset


@method_decorator(signin_required,name="dispatch")
@method_decorator(employer_signin,name='dispatch')
class EmployerEditApplicationView(UpdateView):
    model=Application
    form_class = EditApplicationForm
    template_name = "jobs/application.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("elistapplication")


class EmployerDeleteApplication(DeleteView):

        model=Application
        template_name = "jobs/employerdeleteapplication.html"
        pk_url_kwarg = "id"
        success_url = reverse_lazy("elistapplication")

