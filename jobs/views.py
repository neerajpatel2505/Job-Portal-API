from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from .models import JobPost, Applicant
from .serializers import JobPostSerializer, ApplicantSerializer
from rest_framework.views import APIView

class CreateJobPostView(generics.CreateAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer

class ListJobsView(generics.ListAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer

class ApplyToJobView(APIView):
    def post(self, request, job_id):
        email = request.data.get('email')
        today = timezone.now().date()

        if Applicant.objects.filter(email=email, applied_at__date=today).count() >= 3:
            return Response(
                {"error": "You can apply to only 3 jobs per day."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        try:
            job = JobPost.objects.get(pk=job_id)
        except JobPost.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "name": request.data.get("name"),
            "email": email,
            "resume_link": request.data.get("resume_link"),
            "applied_job": job.id
        }

        serializer = ApplicantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobSummaryView(APIView):
    def get(self, request):
        jobs = JobPost.objects.annotate(
            applicant_count=Count('applicants')
        ).order_by('-applicant_count')

        data = [
            {
                "title": job.title,
                "description": job.description,
                "location": job.location,
                "posted_by": str(job.posted_by),
                "applicant_count": job.applicant_count
            }
            for job in jobs
        ]
        return Response(data, status=status.HTTP_200_OK)
