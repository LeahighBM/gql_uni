import graphene
from graphene_django import DjangoObjectType
from uni_app.models import Student, Faculty, Course
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


class StudentQueries(graphene.ObjectType):
    students = graphene.List(StudentType)
    student  = graphene.Field(StudentType, id=graphene.ID(required=True))

    total_students = graphene.Int()
    num_students_by_year  = graphene.List(YearCountType)
    num_students_by_major = graphene.List(MajorCountType)
    avg_gpa_by_year  = graphene.List(YearAvgGpaType)
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
        aggregate = Student.objects.values('year').annotate(count=Count('id'))

        return [
            YearCountType(year=item['year'], count=item['count'])
            for item in aggregate
        ]
    
    def resolve_num_students_by_major(self, info):
        aggregate = Student.objects.values('major').annotate(count=Count("id"))

        return [
            MajorCountType(major=item['major'], count=item['count'])
            for item in aggregate
        ]
    
    def resolve_avg_gpa_by_year(self, info):
        aggregate = Student.objects.values('year').annotate(avg=Avg('gpa'))

        return [
            YearAvgGpaType(year=item['year'], avg_gpa=item['avg'])
            for item in aggregate
        ]
    
    def resolve_avg_gpa_by_major(self, info):
        aggregate = Student.objects.values('major').annotate(avg=Avg('gpa'))

        return [
            MajorAvgGpaType(major=item['major'], avg_gpa=item['avg'])
            for item in aggregate
        ]

class StudentMutations(graphene.ObjectType):
    create_student = CreateStudent.Field()
    update_student = UpdateStudent.Field()
    delete_student = DeleteStudent.Field()
    

class Query(StudentQueries, graphene.ObjectType):
    pass

class Mutation(StudentMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)