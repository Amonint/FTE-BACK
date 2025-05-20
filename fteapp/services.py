from .models import Student, Class, Enrollment, Grade, Certificate, Payment
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

# Enroll a student in a class
def enroll_student(student: Student, class_obj: Class) -> Enrollment:
    enrollment, created = Enrollment.objects.get_or_create(
        student=student, class_obj=class_obj,
        defaults={'is_active': True}
    )
    return enrollment

# Get all grades for a student
def get_student_grades(student: Student):
    return Grade.objects.filter(enrollment__student=student)

# Generate a certificate for a student
def generate_certificate(student: Student, name: str, description: str = "", file=None) -> Certificate:
    certificate = Certificate.objects.create(
        student=student,
        name=name,
        description=description,
        date_awarded=timezone.now().date(),
        file=file
    )
    return certificate

# Process a payment for a student
def process_payment(student: Student, amount: float, description: str = "", is_matriculation: bool = False, transaction_id: str = "") -> Payment:
    payment = Payment.objects.create(
        student=student,
        amount=amount,
        description=description,
        is_matriculation=is_matriculation,
        transaction_id=transaction_id
    )
    return payment

# Get all classes a student is enrolled in
def get_student_classes(student: Student):
    return Class.objects.filter(enrollments__student=student, enrollments__is_active=True)

# Get all certificates for a student
def get_student_certificates(student: Student):
    return Certificate.objects.filter(student=student) 