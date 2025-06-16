from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    Usuario, RecuperacionContrasena, ActividadUsuario, Materia,
    PeriodoAcademico, Calificacion, Asistencia, Horario,
    ClaseVirtual, Material, Matricula, Notificacion, Recomendacion
)

@admin.register(Usuario)
class UsuarioAdmin(ModelAdmin):
    list_display = ('username', 'cedula', 'email', 'nombre_completo', 'nivel_ingles', 'ultimo_acceso')
    search_fields = ('username', 'cedula', 'email', 'nombre_completo')
    list_filter = ('nivel_ingles',)

@admin.register(RecuperacionContrasena)
class RecuperacionContrasenaAdmin(ModelAdmin):
    list_display = ('usuario', 'fecha_solicitud', 'usado')
    list_filter = ('usado',)

@admin.register(ActividadUsuario)
class ActividadUsuarioAdmin(ModelAdmin):
    list_display = ('usuario', 'tipo_actividad', 'fecha_hora')
    list_filter = ('tipo_actividad',)

@admin.register(Materia)
class MateriaAdmin(ModelAdmin):
    list_display = ('nombre', 'profesor', 'aula')
    search_fields = ('nombre', 'aula')

@admin.register(PeriodoAcademico)
class PeriodoAcademicoAdmin(ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin')
    search_fields = ('nombre',)

@admin.register(Calificacion)
class CalificacionAdmin(ModelAdmin):
    list_display = ('usuario', 'materia', 'periodo', 'nota')
    list_filter = ('periodo', 'materia')
    search_fields = ('usuario__username', 'materia__nombre')

@admin.register(Asistencia)
class AsistenciaAdmin(ModelAdmin):
    list_display = ('usuario', 'materia', 'fecha', 'estado')
    list_filter = ('estado', 'fecha', 'materia')
    search_fields = ('usuario__username', 'materia__nombre')

@admin.register(Horario)
class HorarioAdmin(ModelAdmin):
    list_display = ('dia_semana', 'hora_inicio', 'hora_fin', 'materia')
    list_filter = ('dia_semana', 'materia')

@admin.register(ClaseVirtual)
class ClaseVirtualAdmin(ModelAdmin):
    list_display = ('materia', 'fecha', 'hora_inicio', 'plataforma')
    list_filter = ('plataforma', 'fecha', 'materia')

@admin.register(Material)
class MaterialAdmin(ModelAdmin):
    list_display = ('titulo', 'materia', 'tipo', 'fecha_publicacion')
    list_filter = ('tipo', 'materia')
    search_fields = ('titulo', 'descripcion')

@admin.register(Matricula)
class MatriculaAdmin(ModelAdmin):
    list_display = ('usuario', 'periodo', 'estado')
    list_filter = ('estado', 'periodo', 'materias')
    search_fields = ('usuario__username',)
    filter_horizontal = ('materias',)

@admin.register(Notificacion)
class NotificacionAdmin(ModelAdmin):
    list_display = ('usuario', 'titulo', 'tipo', 'fecha_envio', 'leida')
    list_filter = ('tipo', 'leida')
    search_fields = ('titulo', 'mensaje')

@admin.register(Recomendacion)
class RecomendacionAdmin(ModelAdmin):
    list_display = ('usuario', 'tipo', 'origen', 'fecha_creacion')
    list_filter = ('tipo', 'origen')
    search_fields = ('mensaje',)
