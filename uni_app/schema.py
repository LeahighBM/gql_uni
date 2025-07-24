import graphene
from graphene_django import DjangoObjectType
from uni_app.models import Student, Faculty, Course, Enrollment
from django.db.models import Count, Avg

class StudentType(DjangoObjectType):
    class Meta:
        model  = Student
        fields = "__all__"


class FacultyType(DjangoObjectType):
    class Meta:
        model  = Faculty
        fields = "__all__"


class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        fields = "__all__"


class EnrollmentType(DjangoObjectType):
    class Meta:
        model = Enrollment
        fields = "__all__"


class YearCountType(graphene.ObjectType):
    year  = graphene.String()
    count = graphene.Int()


class MajorCountType(graphene.ObjectType):
    major = graphene.String()
    count = graphene.Int()


class YearAvgGpaType(graphene.ObjectType):
    year    = graphene.String()
    avg_gpa = graphene.Float() 


class MajorAvgGpaType(graphene.ObjectType):
    major   = graphene.String()
    avg_gpa = graphene.Float()


class CreateStudent(graphene.Mutation):
    class Arguments:
        fname = graphene.String(required=True)
        lname = graphene.String(required=True)
        major = graphene.String()
        year  = graphene.String()
        gpa   = graphene.Float() 

    student = graphene.Field(StudentType) 

    def mutate(self, info, fname, lname, year, major=None, gpa=None):
        student = Student(fname=fname, lname=lname, major=major, year=year, gpa=gpa)
        student.save()

        return CreateStudent(student=student)
    
class UpdateStudent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        fname = graphene.String()
        lname = graphene.String()
        major = graphene.String()
        year  = graphene.String()
        gpa   = graphene.Float()
      
    student = graphene.Field(StudentType)

    def mutate(self, info, id, fname=None, lname=None, year=None, major=None, gpa=None):
        try:
            student = Student.objects.get(pk=id)
        except Student.DoesNotExist:
            raise Exception("Student does not exist")
        
        if fname is not None:
            student.fname = fname
        if lname is not None:
            student.lname = lname
        if year is not None:
            student.year = year
        if major is not None:
            student.major = major
        if gpa is not None:
            student.gpa = gpa 

        student.save()
        return UpdateStudent(student=student)
    

class DeleteStudent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True) 

    ok = graphene.Boolean()

    def mutate(self, info, id):
        try: 
            student = Student.objects.get(pk=id)
            student.delete()
            return DeleteStudent(ok=True)
        except Student.DoesNotExist:
            raise Exception(f"Student with id {id} does not exist")
        
class CreateFaculty(graphene.Mutation):
    class Arguments:
        fname      = graphene.String(required=True)
        lname      = graphene.String(required=True)
        department = graphene.String(required=True)

    faculty = graphene.Field(FacultyType)

    def mutate(self, info, fname, lname, department):
        faculty = Faculty(fname=fname, lname=lname, department=department)
        faculty.save() 

        return CreateFaculty(faculty=faculty)
    

class CreateCourse(graphene.Mutation):
    class Arguments:
        name        = graphene.String(required=True)
        course_id   = graphene.String(required=True)
        description = graphene.String(required=True)
        instructor  = graphene.ID(required=True)

    course = graphene.Field(CourseType)

    def mutate(self, info, name, course_id, description, instructor):
        instructor = Faculty.objects.get(pk=instructor)
        course = Course(name=name, 
                        course_id=course_id, 
                        description=description, 
                        instructor=instructor)
        course.save()

        return CreateCourse(course=course)
    

class EnrollStudentInCourse(graphene.Mutation):
    class Arguments:
        course_id  = graphene.ID(required=True)
        student_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    enrollment = graphene.Field(EnrollmentType)

    def mutate(self, info, course_id, student_id):
        try:
            student = Student.objects.get(pk=student_id)
            course  = Course.objects.get(pk=course_id)
        except Student.DoesNotExist:
            raise Exception(f"Student with ID {student_id} does not exist.")
        except Course.DoesNotExist:
            raise Exception(f"Course with ID {course_id} does not exist.")
        
        enrollment = Enrollment(course_id=course, student_id=student)
        enrollment.save()

        return EnrollStudentInCourse(enrollment=enrollment, ok=True)
        


class StudentQueries(graphene.ObjectType):
    students = graphene.List(StudentType)
    student  = graphene.Field(StudentType, id=graphene.ID(required=True))

    total_students = graphene.Int()
    num_students_by_year  = graphene.List(YearCountType)
    num_students_by_major = graphene.List(MajorCountType)
    avg_gpa_by_year  = graphene.List(YearAvgGpaType)
    avg_gpa_by_year_single = graphene.Field(
        YearAvgGpaType, 
        year=graphene.String(required=True))
    avg_gpa_by_major = graphene.List(MajorAvgGpaType)


    def resolve_students(self, info):
        return Student.objects.all()
    
    def resolve_student(self, info, id):
        try:
            return Student.objects.get(pk=id)
        except Student.DoesNotExist:
            raise Exception("Student does not exist")
        
    def resolve_total_students(self, info):
        return Student.objects.count()
    
    def resolve_num_students_by_year(self, info):
        ann = Student.objects.values('year').annotate(count=Count('id'))

        return [
            YearCountType(year=item['year'], count=item['count'])
            for item in ann
        ]
    
    def resolve_num_students_by_major(self, info):
        ann = Student.objects.values('major').annotate(count=Count("id"))

        return [
            MajorCountType(major=item['major'], count=item['count'])
            for item in ann
        ]
    
    def resolve_avg_gpa_by_year(self, info):
        ann = Student.objects.values('year').annotate(avg=Avg('gpa'))

        return [
            YearAvgGpaType(year=item['year'], avg_gpa=item['avg'])
            for item in ann
        ]
    
    def resolve_avg_gpa_by_year_single(self, info, year):
        agg = Student.objects.filter(year=year).aggregate(
            avg=Avg('gpa')
        )

        return YearAvgGpaType(year=year, avg_gpa=agg['avg'])

    def resolve_avg_gpa_by_major(self, info):
        ann = Student.objects.values('major').annotate(avg=Avg('gpa'))

        return [
            MajorAvgGpaType(major=item['major'], avg_gpa=item['avg'])
            for item in ann
        ]
    

class FacultyQueries(graphene.ObjectType):
    all_faculty    = graphene.List(FacultyType)
    faculty_single = graphene.Field(FacultyType,id=graphene.ID(required=True))

    def resolve_all_faculty(self, info):
        return Faculty.objects.all()

    def resolve_faculty_single(self, info, id):
        try:
            return Faculty.objects.get(pk=id)
        except Faculty.DoesNotExist:
            raise Exception("Faculty ID does not exist")
        

class CourseQueries(graphene.ObjectType):
    courses = graphene.List(CourseType)
    course  = graphene.Field(CourseType, id=graphene.ID(required=True))

    def resolve_courses(self, info):
        return Course.objects.all()
    
    def resolve_course(self, info, id):
        try:
            return Course.objects.get(pk=id)
        except Course.DoesNotExist:
            raise Exception("Course ID does not exist")


class EnrollmentQueries(graphene.ObjectType):
    enrollment = graphene.List(EnrollmentType)

    def resolve_enrollment(self, info):
        return Enrollment.objects.all()


class StudentMutations(graphene.ObjectType):
    create_student = CreateStudent.Field()
    update_student = UpdateStudent.Field()
    delete_student = DeleteStudent.Field()


class FacultyMutations(graphene.ObjectType):
    create_faculty = CreateFaculty.Field()


class CourseMutations(graphene.ObjectType):
    create_course = CreateCourse.Field()


class EnrollmentMutations(graphene.ObjectType):
    enroll_student = EnrollStudentInCourse.Field()
    

class Query(StudentQueries, FacultyQueries, CourseQueries, EnrollmentQueries, graphene.ObjectType):
    pass

class Mutation(StudentMutations, FacultyMutations, CourseMutations, EnrollmentMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)