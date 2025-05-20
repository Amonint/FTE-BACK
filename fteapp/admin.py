from django.contrib import admin
from .models import Student, Class, Enrollment, Grade, Certificate, Payment

# Register your models here.
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Enrollment)
admin.site.register(Grade)
admin.site.register(Certificate)
admin.site.register(Payment)
