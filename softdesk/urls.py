from django.urls import path

from softdesk.views import SignUpAPIView, LoginAPIView
from softdesk.views import ProjectsAPIView, ProjectDetailsAPIView, ProjectUsersAPIView
from softdesk.views import ProjectIssuesAPIView, ProjectIssueCommentsAPIView, ProjectIssueCommentDetailsAPIView


urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('projects/', ProjectsAPIView.as_view()),
    path('projects/<int:project_id>/', ProjectDetailsAPIView.as_view()),
    path('projects/<int:project_id>/users/', ProjectUsersAPIView.as_view()),
    path('projects/<int:project_id>/users/<int:user_id>/', ProjectUsersAPIView.as_view()),
    path('projects/<int:project_id>/issues/', ProjectIssuesAPIView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/', ProjectIssuesAPIView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', ProjectIssueCommentsAPIView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/', ProjectIssueCommentDetailsAPIView.as_view()),
]
