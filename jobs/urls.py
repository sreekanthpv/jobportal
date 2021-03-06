from django.urls import path
from jobs import views

urlpatterns = [
    path('users/accounts/signup', views.RegistrationView.as_view(), name="signup"),
    path('users/accounts/signin', views.SignInView.as_view(), name='signin'),
    path('users/accounts/signout',views.SignOutView.as_view(),name='signout'),
    path('employer/employerhome', views.EmployerHome.as_view(), name='employerhome'),
    path('jobseeker/jobseekerhome',views.JobSeekerHomeView.as_view(),name="jobseekerhome"),

    path('employer/company/add',views.AddCompanyView.as_view(),name='addcompany'),
    path('employer/company/view',views.ViewCompanyProfileView.as_view(),name="viewcompanyprofile"),
    path('employer/company/update/<int:id>',views.EditCompanyProfileView.as_view(),name='editcompany'),

    path('employer/jobs/add',views.AddJobView.as_view(),name="addjob"),
    path('employer/jobs/view',views.ListJobView.as_view(),name='listjob'),
    path('employer/jobs/update/<int:id>',views.EditJobView.as_view(),name="editjob"),
    path('employer/jobs/remove/<int:id>',views.DeleteJobs.as_view(),name="deletejob"),
    path('employer/application/view',views.EmployerListApplication.as_view(),name="elistapplication"),
    path('employer/application/update/<int:id>',views.EmployerEditApplicationView.as_view(),name="employereditapp"),
    path('employer/application/delete/<int:id>',views.EmployerDeleteApplication.as_view(),name="deleteapp"),

    path('jobseeker/profile/add',views.AddJobSeekerProfileView.as_view(),name='addjobseekerprofile'),
    path('jobseeker/profile/view',views.ViewJobSeekerProfileVIew.as_view(),name="viewjobseekerprofile"),
    path('jobseeker/profile/update/<int:id>',views.EditJobSeekerProfileView.as_view(),name="editjobseekerprofile"),
    path('jobseeker/jobs/apply/<int:id>',views.JobseekerApplicationView.as_view(),name="application"),
    path('jobseeker/jobs/application/view',views.ListApplicationView.as_view(),name="listapplication"),
    path('jobseeker/jobs/search',views.JobSearch.as_view(),name="jobsearch"),


]
