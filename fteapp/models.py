from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

class Class(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.code})"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'class_obj')

    def __str__(self):
        return f"{self.student} enrolled in {self.class_obj}"

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='grades')
    value = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.enrollment.student} - {self.enrollment.class_obj}: {self.value}"

class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_awarded = models.DateField()
    file = models.FileField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.student}"

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    is_matriculation = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.student} - {self.amount} on {self.payment_date.date()}"
