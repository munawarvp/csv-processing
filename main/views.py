
from rest_framework.views import APIView
from rest_framework.response import Response

from main.serializers import FileUploadSerializer
from main.helper import process_user_data

class UserDataView(APIView):
    def post(self, request):
        try:
            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'success': False, 'message': serializer.errors}, status=400)
            
            file = serializer.validated_data['file']
            data = process_user_data(file)

            return Response({'success': True, 'message': 'Data uploaded successfully.', 'data': data})
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)