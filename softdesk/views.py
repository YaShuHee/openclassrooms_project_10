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

from .models import User, Project, Contribution, Issue, Comment
from .serializers import UserSerializer, ProjectSerializer, ContributionSerializer, IssueSerializer, CommentSerializer


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
                "detail": "You used a wrong username & password combination."
            }
        return Response(data)


class ProjectsAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # TODO: OK
    def get(self, request):
        user = request.user
        contributed = [contribution.project for contribution in Contribution.objects.filter(user=user)]
        owned = Project.objects.filter(author=user)
        projects = list(chain(owned, contributed))
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

    # TODO: OK
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author:
            data = {
                "author": UserSerializer(project.author).data,
                "contributors": [UserSerializer(contributor.user).data for contributor in project.contributors.all()]
            }
            return Response(data)
        else:
            raise Http404

    # TODO: OK
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author:
            user_id = request.data["user"]
            if isinstance(user_id, int):
                # this absolutely needs UniqueConstraint <user-project> on Contribution model
                user = get_object_or_404(User, id=int(user_id))
                if user == project.author:
                    data = {
                        "added": False,
                        "detail": "This user is the project author. They can not be contributor."
                    }
                else:
                    try:
                        contribution = Contribution.objects.create(user=user, project=project)
                        contribution.save()
                        data = {
                            "added": True
                        }
                    except IntegrityError:
                        data = {
                            "added": False,
                            "detail": "This user is already a contributor."
                        }
            else:
                data = {
                    "added": False,
                    "detail": "The 'user_id' field must be an integer."
                }
            return Response(data)
        else:
            raise Http404

    # TODO: OK
    def delete(self, request, project_id, user_id):
        project = get_object_or_404(Project, id=project_id)
        user = get_object_or_404(User, id=user_id)
        if request.user == project.author:
            contribution = get_object_or_404(Contribution, user=user, project=project)
            contribution.delete()
            data = {
                "deleted": True
            }
            return Response(data)
        else:
            raise Http404


class ProjectIssuesAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # TODO
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author or project.contributors.filter(user=request.user).count > 0:
            pass
        else:
            raise Http404

    # TODO
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.author or project.contributors.filter(user=request.user).count > 0:
            pass
        else:
            raise Http404

    # TODO
    def put(self, request, project_id, issue_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        if request.user == project.author or project.contributors.filter(user=request.user).count > 0:
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
        if request.user == project.author or project.contributors.filter(user=request.user).count > 0:
            if request.user == issue.author:
                issue.delete()
                data = {
                    "deleted": True
                }
            else:
                data = {
                    "deleted": False,
                    "detail": "You have the right to read this issue, not to delete it."
                }
            return Response(data)
        else:
            raise Http404


class ProjectIssueCommentsAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # TODO
    def get(self, request, project_id, issue_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        if request.user == project.author or project.contributors.filter(user=request.user).count > 0:
            pass
        else:
            raise Http404

    # TODO
    def post(self, request, project_id, issue_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        if request.user == project.author or project.contributors.filter(user=request.user).count > 0:
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
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == project.author or project.contributors.filter(user=request.user).count > 0:
            pass
        else:
            raise Http404

    # TODO
    def put(self, request, project_id, issue_id, comment_id):
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id)
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == project.author or project.contributors.filter(user=request.user).count > 0:
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
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == project.author or project.contributors.filter(user=request.user).count > 0:
            if request.user == comment.author:
                comment.delete()
                data = {
                    "deleted": True
                }
            else:
                data = {
                    "deleted": False,
                    "detail": "You have the right to read this comment, not to delete it."
                }
            return Response(data)
        else:
            raise Http404
