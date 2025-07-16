from django.test import TestCase
from graphene.test import Client
from uni_app.models import Student
from uni_app.schema import schema

# Create your tests here.

class StudentQueryTests(TestCase):
    def setUp(self):
        Student.objects.create(fname="Testy", 
                               lname="McTestface", 
                               year="Sophomore",
                               major="Business", 
                               gpa=3.58)

        Student.objects.create(fname="John", 
                               lname="Doe", 
                               year="Junior",
                               major="Economics", 
                               gpa=2.7)
        
        self.client = Client(schema)

    def test_resolve_all_students(self):
        query = """
        {
            students {
                fname,
                lname,
                year,
                major,
                gpa            
            }
        }
        """

        exe = self.client.execute(query)

        self.assertIsNone(exe.get("errors"))
        self.assertEqual(len(exe["data"]["students"]), 2)

    def test_resolve_single_student_success(self):
        query = """
            {
                student(id: 1) {
                id,
                fname,
                lname,
                year,
                major,
                gpa               
                }
            }
        """

        exe = self.client.execute(query)

        self.assertIsNone(exe.get("errors"))
        self.assertEqual(len(exe["data"]), 1)
        self.assertEqual(exe["data"]["student"]["id"], "1")
        self.assertEqual(exe["data"]["student"]["fname"], "Testy")

    def test_resolve_single_student_failure(self):
        query = """
            {
                student(id: 3) {
                id,
                fname,
                lname,
                year,
                major,
                gpa               
                }
            }
        """

        exe = self.client.execute(query)

        self.assertIsNotNone(exe.get("errors"))