from rest_framework import generics, status, viewsets
from rest_framework.response import Response

import base64

from .model.recog import class_labels, return_mood


# Create your views here.
class MoodDetector(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        mood = "Error try again"

        image_data = data.get('image')
        if image_data:
            image_data = image_data.split(',')[1]
            image_data = base64.b64decode(image_data)
            print(image_data)
            file_name = "../media/mood_image.jpg"
            with open(file_name, 'wb') as f:
                f.write(image_data)

            # model_op = return_mood(file_name)
            # if isinstance(model_op, int):
            #     mood = class_labels[int(model_op)]

        return Response({"mood": mood}, status=status.HTTP_200_OK)