from rest_framework.serializers import ModelSerializer

from .models import User, Project, Issue, Contributors, Comments


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
        extra_kwargs = {
            "author": {"read_only": True},
            "created_time": {"read_only": True}
        }


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        extra_kwargs = {
            "author": {"read_only": True},
            "created_time": {"read_only": True}
        }


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"
        extra_kwargs = {
            "author": {"read_only": True},
            "created_time": {"read_only": True}
        }


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = "__all__"
