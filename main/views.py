import csv
from io import TextIOWrapper

from rest_framework.views import APIView
from rest_framework.response import Response

from main.serializers import FileUploadSerializer, UserSerializer

class UserDataView(APIView):

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
        else:
            return Response({'success': False, 'message': serializer.errors})

        try:
            

            return Response({'success': True, 'message': 'Data uploaded successfully.'})
        except Exception as e:
            return Response({'success': False, 'message': str(e)})