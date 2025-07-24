from django.db import models

# Create your models here.

class Student(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    year  = models.CharField(max_length=30)
    major = models.CharField(max_length=100, null=True) 
    gpa   = models.FloatField(null=True)

    def __str__(self):
        return self.fname + " " + self.lname


class Faculty(models.Model):
    fname      = models.CharField(max_length=100)
    lname      = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self): 
        return self.fname + " " + self.lname


class Course(models.Model):
    name        = models.CharField(max_length=255)
    course_id   = models.CharField(max_length=10)
    description = models.TextField()
    instructor  = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self): 
        return self.name
    

class Enrollment(models.Model):
    course_id  = models.ForeignKey(Course,  on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_id