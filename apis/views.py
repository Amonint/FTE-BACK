from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
import logging
from fteapp.models import (
    Usuario, Materia, PeriodoAcademico, Calificacion,
    Asistencia, Horario, ClaseVirtual, Material,
    Matricula, Notificacion, Recomendacion
)
from .serializers import (
    UsuarioSerializer, MateriaSerializer, PeriodoAcademicoSerializer,
    CalificacionSerializer, AsistenciaSerializer, HorarioSerializer,
    ClaseVirtualSerializer, MaterialSerializer, MatriculaSerializer,
    NotificacionSerializer, RecomendacionSerializer
)

logger = logging.getLogger(__name__)

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        logger.info(f"Datos recibidos en registro: {request.data}")
        serializer = UsuarioSerializer(data=request.data)
        
        if serializer.is_valid():
            logger.info(f"Datos validados: {serializer.validated_data}")
            try:
                # Create and save user
                user = serializer.save()
                logger.info(f"Usuario creado exitosamente: {user.username}")
                
                # Generate token
                refresh = RefreshToken.for_user(user)
                return Response({
                    'token': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UsuarioSerializer(user).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error al crear usuario: {str(e)}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error(f"Errores de validación: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        logger.info(f"Intento de login - Usuario: {username}")
        logger.info(f"Datos recibidos en login: {request.data}")

        if not username or not password:
            return Response(
                {'error': 'Por favor proporcione username y password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar si el usuario existe
        try:
            user_exists = Usuario.objects.filter(username=username).exists()
            logger.info(f"¿Usuario existe en BD?: {user_exists}")
            if user_exists:
                user_obj = Usuario.objects.get(username=username)
                logger.info(f"Hash de contraseña almacenado: {user_obj.password[:20]}...")
        except Exception as e:
            logger.error(f"Error al verificar usuario: {str(e)}")

        # Usar authenticate de Django
        user = authenticate(username=username, password=password)
        logger.info(f"Resultado de authenticate: {'éxito' if user else 'fallido'}")
        
        if user is not None and user.is_active:
            logger.info(f"Usuario autenticado correctamente: {user.username}")
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UsuarioSerializer(user).data
            })
        else:
            logger.warning(f"Credenciales inválidas para usuario: {username}")
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Usuario.objects.all()
        if not self.request.user.is_staff:
            return queryset.filter(id=self.request.user.id)
        return queryset

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    permission_classes = [permissions.IsAuthenticated]

class PeriodoAcademicoViewSet(viewsets.ModelViewSet):
    queryset = PeriodoAcademico.objects.all()
    serializer_class = PeriodoAcademicoSerializer
    permission_classes = [permissions.IsAuthenticated]

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Calificacion.objects.all()
        if not self.request.user.is_staff:
            return queryset.filter(usuario=self.request.user)
        return queryset

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Asistencia.objects.all()
        if not self.request.user.is_staff:
            return queryset.filter(usuario=self.request.user)
        return queryset

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClaseVirtualViewSet(viewsets.ModelViewSet):
    queryset = ClaseVirtual.objects.all()
    serializer_class = ClaseVirtualSerializer
    permission_classes = [permissions.IsAuthenticated]

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Matricula.objects.all()
        if not self.request.user.is_staff:
            return queryset.filter(usuario=self.request.user)
        return queryset

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Notificacion.objects.all()
        if not self.request.user.is_staff:
            return queryset.filter(usuario=self.request.user)
        return queryset

    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        notificacion = self.get_object()
        notificacion.leida = True
        notificacion.save()
        return Response({'status': 'notificación marcada como leída'})

class RecomendacionViewSet(viewsets.ModelViewSet):
    queryset = Recomendacion.objects.all()
    serializer_class = RecomendacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Recomendacion.objects.all()
        if not self.request.user.is_staff:
            return queryset.filter(usuario=self.request.user)
        return queryset
