from rest_framework.serializers import ModelSerializer

from .models import User, Project, Issue, Contribution, Comment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
        extra_kwargs = {
            "password": {"write_only": True}
        }


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


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "author": {"read_only": True},
            "created_time": {"read_only": True}
        }


class ContributionSerializer(ModelSerializer):
    class Meta:
        model = Contribution
        fields = "__all__"
