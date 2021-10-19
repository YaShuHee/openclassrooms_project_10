from django.db import models
from django.contrib.auth.models import User


class Issue(models.Model):
    TAG_CHOICES = [
        ("B", "BUG"),
        ("E", "ENHANCEMENT"),
        ("T", "TASK"),
    ]

    PRIORITY_CHOICES = [
        ("W", "WEAK"),
        ("M", "MEDIUM"),
        ("H", "HIGH"),
    ]

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    tag = models.CharField(max_length=1, choices=TAG_CHOICES, default=TAG_CHOICES[0][0])
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=PRIORITY_CHOICES[0][0])
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="issues")
    status = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="owned_issues", null=True)
    assigned = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="assigned_issues", null=True)
    created_time = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    type = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.CharField(max_length=1000)
    issue = models.ForeignKey("Issue", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")


class Contributors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contributions")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="contributors")
