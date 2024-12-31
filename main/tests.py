from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

class UserDataViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = 'http://localhost:8000/api/user-data'
        self.valid_csv_content = (
            "username,email,age\n"
            "testuser1,test1@example.com,25\n"
            "testuser2,test2@example.com,30\n"
        )
        self.invalid_csv_content = (
            "username,email,age\n"
            "testuser1,test1@example.com,not_a_number\n"  # Invalid age
            ",,\n"  # Empty row
        )

    
    def test_upload_valid_csv(self):
        """Test uploading a valid CSV file."""
        file = SimpleUploadedFile("valid_users.csv", self.valid_csv_content.encode(), content_type="text/csv")
        response = self.client.post(self.url, {'file': file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['records_saved'], 2)

    def test_upload_invalid_csv(self):
        """Test uploading an invalid CSV file."""
        file = SimpleUploadedFile("invalid_users.csv", self.invalid_csv_content.encode(), content_type="text/csv")
        response = self.client.post(self.url, {'file': file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['records_saved'], 0)
        self.assertEqual(response.data['data']['records_rejected'], 1)
        self.assertEqual(len(response.data['data']['validation_errors']), 1)

    def test_invalid_file_format(self):
        """Test uploading a non-CSV file."""
        file = SimpleUploadedFile("invalid_file.txt", b"Invalid content", content_type="text/plain")
        response = self.client.post(self.url, {'file': file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('file', response.data['message'])
        self.assertEqual(response.data['message']['file'][0], "The uploaded file must be a CSV file.")