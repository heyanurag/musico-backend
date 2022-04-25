from rest_framework import generics, status, permissions
from rest_framework.response import Response
# from django.contrib.auth.models import AnonymousUser

import base64

from .model.recog import class_labels, return_mood
from .helper import getSearchTracks, getTracksByMood
from authentication.models import User

# Create your views here.


class MoodDetector(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        data = request.data
        mood = "Error try again"
        tracks = []

        image_data = data.get('image')
        if image_data:
            image_data = image_data.split(',')[1]
            image_data = base64.b64decode(image_data)
            file_name = "mood_image.jpg"
            with open(file_name, 'wb') as f:
                f.write(image_data)

            model_op = return_mood(file_name)
            if isinstance(model_op, int):
                mood = class_labels[int(model_op)]
                if User.objects.filter(id=request.user.pk):
                    User.objects.filter(id=request.user.pk).update(mood=str(mood))

                tracks = getTracksByMood(mood)

        return Response({"mood": mood, "tracks": tracks}, status=status.HTTP_200_OK)


class PopularMusicByMood(generics.GenericAPIView):
    model = User
    permissions = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get(self, request):
        user = self.get_object()

        if type(user) != User:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        tracks = getTracksByMood(user.mood)

        return Response({"tracks": tracks}, status=status.HTTP_200_OK)


class SearchTracks(generics.GenericAPIView):
    model = User
    permissions = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        obj = self.request.user

        return obj

    def get(self, request):
        user = self.get_object()

        if type(user) != User:
            return Response({"message": "Unathorized"}, status=status.HTTP_401_UNAUTHORIZED)

        searchQuery = request.query_params.get("searchQuery")
        
        if not searchQuery or not isinstance(searchQuery, str):
            return Response({"message": "searchQuery is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(searchQuery) < 3:
            return Response({"message": "searchQuery length must be greater than or equal to 3 characters"}, status=status.HTTP_400_BAD_REQUEST)
 
        tracks = getSearchTracks(searchQuery)

        return Response({"tracks": tracks}, status=status.HTTP_200_OK)
