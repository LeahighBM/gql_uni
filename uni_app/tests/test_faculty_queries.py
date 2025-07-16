from django.test import TestCase
from graphene.test import Client
from uni_app.models import Faculty
from uni_app.schema import schema

# Create your tests here.

class StudentQueryTests(TestCase):
    def setUp(self):
        Faculty.objects.create(fname="Bob",
                               lname="Bobson",
                               department="History")
        Faculty.objects.create(fname="Diane",
                               lname="Dilbopper",
                               department="Psychology")
        
        self.client = Client(schema)

    def test_resolve_all_faculty(self):
        query = """
            {
                allFaculty{
                    fname,
                    lname,
                    department
                }
            }
        """

        exe = self.client.execute(query)

        self.assertIsNone(exe.get("errors"))
        self.assertEqual(len(exe['data']['allFaculty']), 2)
        