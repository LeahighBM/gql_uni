from django.test import TestCase
from graphene.test import Client
from uni_app.models import Student
from uni_app.schema import schema

class StudentMutationTests(TestCase):
    def setUp(self):
        self.client = Client(schema)

    def test_create_student(self):
        mutation = """
            mutation {
                createStudent (
                    fname: "Barbara",
                    lname: "Walters",
                    major: "Journalism",
                    year: "Senior",
                    gpa: 4.0
                )
                {
                    student {
                    id,
                    fname,
                    lname,
                    major,
                    year,
                    gpa
                    }
                }
            }
        """

        exe = self.client.execute(mutation)

        self.assertIsNone(exe.get("errors"))
        self.assertEqual(exe["data"]["createStudent"]["student"]["fname"], "Barbara")
