import re

from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def validate_file(self, value):
        # Check if the file has a CSV extension
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("The uploaded file must be a CSV file.")
        return value


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    age = serializers.IntegerField()

    def validate_email(self, value):
        # check email is correct format
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_age(self, value):
        # check age is between 0 and 120
        if value < 0 or value > 120:
            raise serializers.ValidationError("Age must be between 0 and 120.")
        return value
        