from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthViewSet, UsuarioViewSet, MateriaViewSet, PeriodoAcademicoViewSet,
    CalificacionViewSet, AsistenciaViewSet, HorarioViewSet, ClaseVirtualViewSet,
    MaterialViewSet, MatriculaViewSet, NotificacionViewSet, RecomendacionViewSet
)

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'usuarios', UsuarioViewSet)
router.register(r'materias', MateriaViewSet)
router.register(r'periodos', PeriodoAcademicoViewSet)
router.register(r'calificaciones', CalificacionViewSet)
router.register(r'asistencias', AsistenciaViewSet)
router.register(r'horarios', HorarioViewSet)
router.register(r'clases-virtuales', ClaseVirtualViewSet)
router.register(r'materiales', MaterialViewSet)
router.register(r'matriculas', MatriculaViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'recomendaciones', RecomendacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
