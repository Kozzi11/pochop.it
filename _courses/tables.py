import django_tables2 as tables
from _courses.models import Course


class CourseTable(tables.Table):
    class Meta:
        model = Course
        # add class="paleblue" to <table> tag
        # attrs = {"class": "table"}
        orderable = True
        fields = ('name', 'description')
