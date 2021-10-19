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


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = "__all__"
