import csv
from io import TextIOWrapper

from main.models import User

from main.serializers import UserSerializer

def process_user_data(file):
    data = {
        'records_saved': 0,
        'records_rejected': 0,
        'validation_errors': []
    }
    try:
        csv_file = TextIOWrapper(file, encoding='utf-8')
        user_data = csv.DictReader(csv_file)

        for user in user_data:
            # skip empty rows
            if not any(user.values()):
                continue
            user_serializer = UserSerializer(data=user)
            if user_serializer.is_valid():
                User.objects.create_user(**user_serializer.validated_data)
                data['records_saved'] += 1
            else:
                data['records_rejected'] += 1
                data['validation_errors'].append(user_serializer.errors)

        return data
    except Exception as e:
        raise e