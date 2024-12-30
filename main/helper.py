

def process_user_create():
    try:
        csv_file = TextIOWrapper(file, encoding='utf-8')
        user_data = csv.DictReader(csv_file)

        for user in user_data:
            user_serializer = UserSerializer(data=user)
            if user_serializer.is_valid():
                User.objects.create(**user_serializer.validated_data)
    
    except Exception as e:
        return Response({'success': False, 'message': str(e)})