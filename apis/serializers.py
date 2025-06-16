from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from fteapp.models import (
    Usuario, Materia, PeriodoAcademico, Calificacion,
    Asistencia, Horario, ClaseVirtual, Material,
    Matricula, Notificacion, Recomendacion
)

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password', 'cedula', 'email', 'nombre_completo', 
                 'foto', 'nivel_ingles', 'ultimo_acceso', 'horario']
        read_only_fields = ['ultimo_acceso']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class MateriaSerializer(serializers.ModelSerializer):
    profesor_nombre = serializers.CharField(source='profesor.nombre_completo', read_only=True)

    class Meta:
        model = Materia
        fields = ['id', 'nombre', 'profesor', 'profesor_nombre', 'aula']

class PeriodoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoAcademico
        fields = ['id', 'nombre', 'fecha_inicio', 'fecha_fin']

class CalificacionSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='usuario.nombre_completo', read_only=True)
    materia_nombre = serializers.CharField(source='materia.nombre', read_only=True)
    periodo_nombre = serializers.CharField(source='periodo.nombre', read_only=True)

    class Meta:
        model = Calificacion
        fields = ['id', 'usuario', 'estudiante_nombre', 'materia', 'materia_nombre',
                 'periodo', 'periodo_nombre', 'nota', 'observacion']

class AsistenciaSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='usuario.nombre_completo', read_only=True)
    materia_nombre = serializers.CharField(source='materia.nombre', read_only=True)

    class Meta:
        model = Asistencia
        fields = ['id', 'usuario', 'estudiante_nombre', 'materia', 'materia_nombre',
                 'fecha', 'estado']

class HorarioSerializer(serializers.ModelSerializer):
    materia_nombre = serializers.CharField(source='materia.nombre', read_only=True)

    class Meta:
        model = Horario
        fields = ['id', 'dia_semana', 'hora_inicio', 'hora_fin', 'materia', 'materia_nombre']

class ClaseVirtualSerializer(serializers.ModelSerializer):
    materia_nombre = serializers.CharField(source='materia.nombre', read_only=True)

    class Meta:
        model = ClaseVirtual
        fields = ['id', 'materia', 'materia_nombre', 'fecha', 'hora_inicio',
                 'enlace', 'plataforma']

class MaterialSerializer(serializers.ModelSerializer):
    materia_nombre = serializers.CharField(source='materia.nombre', read_only=True)

    class Meta:
        model = Material
        fields = ['id', 'materia', 'materia_nombre', 'titulo', 'descripcion',
                 'tipo', 'url_archivo', 'fecha_publicacion']

class MatriculaSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='usuario.nombre_completo', read_only=True)
    periodo_nombre = serializers.CharField(source='periodo.nombre', read_only=True)
    materias_info = MateriaSerializer(source='materias', many=True, read_only=True)

    class Meta:
        model = Matricula
        fields = ['id', 'usuario', 'estudiante_nombre', 'periodo', 'periodo_nombre',
                 'estado', 'materias', 'materias_info']

class NotificacionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre_completo', read_only=True)

    class Meta:
        model = Notificacion
        fields = ['id', 'usuario', 'usuario_nombre', 'titulo', 'mensaje',
                 'tipo', 'fecha_envio', 'leida']

class RecomendacionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre_completo', read_only=True)

    class Meta:
        model = Recomendacion
        fields = ['id', 'usuario', 'usuario_nombre', 'mensaje', 'tipo',
                 'fecha_creacion', 'origen'] 