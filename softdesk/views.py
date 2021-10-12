from rest_framework.response import Response
from rest_framework.views import APIView


class SignUpAPIView(APIView):
    def post(self, request):
        pass


class LoginAPIView(APIView):
    def post(self, request):
        pass


class ProjectsAPIView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass


class ProjectDetailsAPIView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request):
        pass


class ProjectUsersAPIView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request, user_id):
        pass


class ProjectIssuesAPIView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request, issue_id):
        pass

    def delete(self, request, issue_id):
        pass


class ProjectIssueCommentsAPIView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass


class ProjectIssueCommentDetailsAPIView(APIView):
    def get(self, request, comment_id):
        pass

    def put(self, request, comment_id):
        pass

    def delete(self, request, comment_id):
        pass
