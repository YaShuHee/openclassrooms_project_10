from itertools import chain

from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from .models import User, Project, Issue, Comments, Contributors
from .serializers import ProjectSerializer


class SignUpAPIView(APIView):
    # TODO: OK
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            data = {
                "created": False,
                "detail": "An account with this username already exists.",
                "username": username
            }
        else:
            user.save()
            data = {
                "created": True,
                "id": user.id,
                "username": username
            }
        return Response(data)


class LoginAPIView(APIView):
    # TODO: OK
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            data = {
                "logged_in": True,
                "token": token
            }
        else:
            data = {
                "logged_in": False,
                "detail": "Bad username & password combination."
            }
        return Response(data)


class ProjectsAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # TODO: OK
    def get(self, request):
        user = request.user
        contributing = [contribution.user for contribution in Contributors.objects.filter(user=user)]
        owning = Project.objects.filter(author=user)
        projects = list(chain(contributing, owning))
        data = {
            "results": [ProjectSerializer(project).data for project in projects]
        }
        return Response(data)

    # TODO: OK
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = Project.objects.create(**serializer.validated_data, author=request.user)
            project.save()
            data = {
                "created": True,
                "id": project.id,
                "created_time": project.created_time
            }
        else:
            data = {
                "created": False,
                "detail": serializer.errors
            }
        return Response(data)


class ProjectDetailsAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # TODO: OK
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author:
            return Response(ProjectSerializer(project).data)
        else:
            raise Http404

    # TODO: OK
    def put(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                keys = ["title", "description", "type"]
                for key in keys:
                    project.__setattr__(key, serializer.validated_data[key])
                project.save()
                data = {"modified": True}
            else:
                data = {
                    "modified": False,
                    "detail": serializer.errors
                }
            return Response(data)
        else:
            raise Http404

    # TODO: OK
    def delete(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author:
            project.delete()
            data = {
                "deleted": True,
                "id": project_id
            }
            return Response(data)
        else:
            raise Http404


class ProjectUsersAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # TODO
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author:
            pass
        else:
            raise Http404

    # TODO
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author:
            pass
        else:
            raise Http404

    # TODO
    def delete(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author:
            pass
        else:
            raise Http404


class ProjectIssuesAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # TODO
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author or request.user in project.contributors:
            pass
        else:
            raise Http404

    # TODO
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author or request.user in project.contributors:
            pass
        else:
            raise Http404

    # TODO
    def put(self, request, project_id, issue_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        if request.user == project.author or request.user in project.contributors:
            if request.user == issue.author:
                pass
            else:
                data = {
                    "modified": False,
                    "detail": "You have the right to read this issue, not to modify it."
                }
                pass
        else:
            raise Http404

    # TODO
    def delete(self, request, project_id, issue_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        if request.user == project.author or request.user in project.contributors:
            if request.user == issue.author:
                pass
            else:
                data = {
                    "deleted": False,
                    "detail": "You have the right to read this issue, not to delete it."
                }
                pass
        else:
            raise Http404


class ProjectIssueCommentsAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # TODO
    def get(self, request, project_id, issue_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        if request.user == project.author or request.user in project.contributors:
            pass
        else:
            raise Http404

    # TODO
    def post(self, request, project_id, issue_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        if request.user == project.author or request.user in project.contributors:
            pass
        else:
            raise Http404


class ProjectIssueCommentDetailsAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # TODO
    def get(self, request, project_id, issue_id, comment_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        comment = get_object_or_404(Comments, id=comment_id)
        if request.user == project.author or request.user in project.contributors:
            pass
        else:
            raise Http404

    # TODO
    def put(self, request, project_id, issue_id, comment_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        comment = get_object_or_404(Comments, id=comment_id)
        if request.user == project.author or request.user in project.contributors:
            if request.user == comment.author:
                pass
            else:
                data = {
                    "modified": False,
                    "detail": "You have the right to read this comment, not to modify it."
                }
                pass
        else:
            raise Http404

    # TODO
    def delete(self, request, project_id, issue_id, comment_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        comment = get_object_or_404(Comments, id=comment_id)
        if request.user == project.author or request.user in project.contributors:
            if request.user == comment.author:
                pass
            else:
                data = {
                    "modified": False,
                    "detail": "You have the right to read this comment, not to delete it."
                }
                pass
        else:
            raise Http404
