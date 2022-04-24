from rest_framework import generics, status, permissions
from rest_framework.response import Response

import base64

from .model.recog import class_labels, return_mood
from .helper import getTracksByMood
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
