from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
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
import logging

logger = logging.getLogger(__name__)

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        logger.debug(f"Login attempt for username: {username}")
        logger.debug(f"Password length: {len(password) if password else 0}")

        if not username or not password:
            return Response(
                {'error': 'Por favor proporcione username y password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to get the user first
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            logger.debug(f"User found: {user.username}")
            logger.debug(f"Stored password hash: {user.password[:20]}...")  # Only log first 20 chars of hash
            
            # Try manual password verification first
            if user.check_password(password):
                logger.debug("Manual password check succeeded")
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'token': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UsuarioSerializer(user).data
                })
            else:
                logger.debug("Manual password check failed")
                return Response(
                    {'error': 'Credenciales inválidas'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
        except User.DoesNotExist:
            logger.debug(f"User not found: {username}")
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            logger.debug(f"Registration data valid for username: {request.data.get('username')}")
            try:
                # Use the serializer's create method which properly handles password
                user = serializer.save()
                logger.debug(f"User created successfully: {user.username}")
                logger.debug(f"Password was hashed: {user.password[:20]}...")  # Only log first 20 chars of hash
                
                # Verify the password works
                if not user.check_password(request.data.get('password')):
                    logger.error("Password verification failed immediately after creation!")
                else:
                    logger.debug("Password verification successful")
                
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'token': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error creating user: {str(e)}")
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        logger.debug(f"Registration validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
