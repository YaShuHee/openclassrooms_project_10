from itertools import chain

from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from .models import User, Project, Issue, Comments, Contributors
from .serializers import UserSerializer, ProjectSerializer, IssueSerializer, CommentsSerializer, ContributorsSerializer


class SignUpAPIView(APIView):
    def post(self, request):
        """ Return username and status : successful or failed (if failed, details)."""
        username = request.data["username"]
        password = request.data["password"]
        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            data = {
                "created": "false",
                "detail": "An account with this username already exists."
            }
        else:
            user.save()
            data = {
                "created": "true",
                "detail": "Account successfully created.",
                "id": user.id,
                "username": username
            }
        return Response(data)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            data = {"token": token}
        else:
            data = {"detail": "Bad username/password combination."}
        return Response(data)


class ProjectsAPIView(APIView):
    KEYS = [
        "title",
        "description",
        "type",
        "author",
    ]

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        contributing = [contribution.user for contribution in Contributors.objects.filter(user=user)]
        owning = Project.objects.filter(author=user)
        projects = list(chain(contributing, owning))
        data = {
            "results": [ProjectSerializer(project).data for project in projects]
        }
        return Response(data)

    def post(self, request):
        try:
            request_data = {key: request.data[key] for key in self.KEYS}
        except KeyError as e:
            data = {
                "created": "false",
                "detail": f"Missing '{e.args[0]}'."
            }
        else:
            project = Project.objects.create(**request_data)
            project.save()
            # return ID and CREATION_DATE (titre)
            data = {
                "created": "true",
                "id": project.id,
                "created_time": project.created_time
            }
        return Response(data)


class ProjectDetailsAPIView(APIView):
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        return Response(ProjectSerializer(project).data)

    def put(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author:
            Project.objects.filter(id=project_id).update(**request.data)
            project.save()
            data = ProjectSerializer(project).data
            data.update({
                "modified": "true",
                "detail": f"Project {project_id} modified."
            })
        else:
            data = {
                "modified": "false",
                "detail": f"You are not the project {project_id} author."
            }
        return Response(data)

    def delete(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author:
            project.delete()
            data = {
                "deleted": "true",
                "detail": f"Project {project_id} deleted."
            }
        else:
            data = {
                "deleted": "false",
                "detail": f"You are not the project {project_id} author."
            }
        return Response(ProjectSerializer(project).data)


class ProjectUsersAPIView(APIView):
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

    def delete(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)


class ProjectIssuesAPIView(APIView):
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

    def put(self, request, project_id, issue_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)

    def delete(self, request, project_id, issue_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)


class ProjectIssueCommentsAPIView(APIView):
    def get(self, request, project_id, issue_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)

    def post(self, request, project_id, issue_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)


class ProjectIssueCommentDetailsAPIView(APIView):
    def get(self, request, project_id, issue_id, comment_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        comment = get_object_or_404(Comments, id=comment_id)

    def put(self, request, project_id, issue_id, comment_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        comment = get_object_or_404(Comments, id=comment_id)

    def delete(self, request, project_id, issue_id, comment_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        comment = get_object_or_404(Comments, id=comment_id)
