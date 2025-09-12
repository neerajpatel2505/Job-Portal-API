"""
URL configuration for job_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from django.urls import path
from jobs.views import CreateJobPostView, ListJobsView, ApplyToJobView, JobSummaryView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', CreateJobPostView.as_view(), name='create-job'),
    path('', ListJobsView.as_view(), name='list-jobs'),
    path('<int:job_id>/apply/', ApplyToJobView.as_view(), name='apply-job'),
    path('summary/', JobSummaryView.as_view(), name='job-summary'),
]


