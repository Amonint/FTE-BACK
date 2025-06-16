from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Usuario(AbstractUser):
    cedula = models.CharField(max_length=20, unique=True, null=False)
    correo = models.EmailField(unique=True, null=False)
    nombre_completo = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    nivel_ingles = models.CharField(max_length=50, null=True, blank=True)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    horario = models.ForeignKey('Horario', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    # Override the email field to use correo
    email = None  # Disable the email field from AbstractUser
    REQUIRED_FIELDS = ['cedula', 'correo', 'nombre_completo']  # Required for createsuperuser

    class Meta:
        db_table = 'usuario'

    def save(self, *args, **kwargs):
        # Update last access time on save
        if not self.pk:  # Only on creation
            self.ultimo_acceso = timezone.now()
        super().save(*args, **kwargs)

class RecuperacionContrasena(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)

    class Meta:
        db_table = 'recuperacion_contrasena'

class ActividadUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_actividad = models.CharField(max_length=50)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'actividad_usuario'

class Materia(models.Model):
    nombre = models.CharField(max_length=255)
    profesor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    aula = models.CharField(max_length=50)

    class Meta:
        db_table = 'materia'

class PeriodoAcademico(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        db_table = 'periodo_academico'

class Calificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    periodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    observacion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'calificacion'

class Asistencia(models.Model):
    ESTADO_CHOICES = [
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('justificado', 'Justificado'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)

    class Meta:
        db_table = 'asistencia'

class Horario(models.Model):
    DIA_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    
    dia_semana = models.CharField(max_length=20, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    class Meta:
        db_table = 'horario'

class ClaseVirtual(models.Model):
    PLATAFORMA_CHOICES = [
        ('zoom', 'Zoom'),
        ('meet', 'Meet'),
    ]
    
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    enlace = models.URLField()
    plataforma = models.CharField(max_length=20, choices=PLATAFORMA_CHOICES)

    class Meta:
        db_table = 'clase_virtual'

class Material(models.Model):
    TIPO_CHOICES = [
        ('libro', 'Libro'),
        ('actividad', 'Actividad'),
        ('video', 'Video'),
    ]
    
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    url_archivo = models.URLField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'material'

class Matricula(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('finalizada', 'Finalizada'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    periodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    materias = models.ManyToManyField(Materia, related_name='matriculas')

    class Meta:
        db_table = 'matricula'

class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('recordatorio', 'Recordatorio'),
        ('administrativo', 'Administrativo'),
        ('academico', 'Académico'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    class Meta:
        db_table = 'notificacion'

class Recomendacion(models.Model):
    TIPO_CHOICES = [
        ('motivacional', 'Motivacional'),
        ('academico', 'Académico'),
    ]
    
    ORIGEN_CHOICES = [
        ('sistema', 'Sistema'),
        ('manual', 'Manual'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    origen = models.CharField(max_length=20, choices=ORIGEN_CHOICES)

    class Meta:
        db_table = 'recomendacion' 