from django.urls import path
from jobs import views

urlpatterns = [
    path('users/accounts/signup', views.RegistrationView.as_view(), name="signup"),
    path('users/accounts/signin', views.SignInView.as_view(), name='signin'),
    path('users/accounts/signout',views.SignOutView.as_view(),name='signout'),
    path('employer/employerhome', views.EmployerHome.as_view(), name='employerhome'),
    path('jobseeker/jobseekerhome',views.JobSeekerHomeView.as_view(),name="jobseekerhome"),
    path('employer/company/add',views.AddCompanyView.as_view(),name='addcompany'),
    path('employer/jobs/add',views.AddJobView.as_view(),name="addjob"),
    path('employer/jobs/view',views.ListJobView.as_view(),name='listjob'),
    path('employer/jobs/update/<int:id>',views.EditJobView.as_view(),name="editjob"),


    path('jobseeker/profile/add',views.AddJobSeekerProfileView.as_view(),name='addjobseekerprofile'),
    path('jobseeker/profile/view',views.ViewJobSeekerProfileVIew.as_view(),name="viewjobseekerprofile"),

]
