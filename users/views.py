from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action


from users.permissions import IsAdminOrReadOnly, IsUserOrAdmin
from users.authentication import CustomAuthBackend
from users.models import User, Balance
from users.serializers import UserSerializer, RegistrationUserSerializer, BalanceSerializer
 

class RegisterAPIView(CreateAPIView):

    serializer_class = RegistrationUserSerializer  # Указываем сериализатор, который будет использоваться для создания пользователя

    def get(self, request, *args, **kwargs):
        # Возвращаем описание страницы регистрации
        return Response({'message': 'Регистрация пользователей'}, status=status.HTTP_200_OK)

    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        login(request=request, user=user)

        # Генерация JWT токенов
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username
        })

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def get(self, request):
        return Response({'message': 'Авторизация пользователей'})
    

    def post(self, request):
        username = request.data.get('username', None)

        password = request.data.get('password', None)

        if username is None or password is None:
            return Response({'error': 'Нужен и логин, и пароль'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomAuthBackend.authenticate(request=request, username=username, password=password)
        if user is None:
            return Response({'error': 'Неверные данные'},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username
        })

        login(request=request, user=user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
        

class LogoutAPIView(APIView):
    def post(self, request):

        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Необходим Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({'error': 'Неверный Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Выход успешен'}, status=status.HTTP_200_OK)
    

class UsersViewSet(ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

class UserView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly, IsUserOrAdmin]


    @action(
        methods=["GET", "PUT", "DELETE"],
        detail=True,
        permission_classes= [IsAuthenticated, IsAdminOrReadOnly],
        serializer_class=BalanceSerializer
    )
    def balance(self, request, pk):
        user = self.get_object()
        serializer = BalanceSerializer(user.balance)
        return Response(serializer.data)

