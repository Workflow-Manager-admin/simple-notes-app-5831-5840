from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Note
from .serializers import NoteSerializer, UserRegistrationSerializer, LoginSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_summary="Health check endpoint",
    operation_description="API health/status check.",
    tags=["health"],
    responses={200: openapi.Response("Health OK", schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={"message": openapi.Schema(type=openapi.TYPE_STRING)}))}
)
@api_view(['GET'])
def health(request):
    """API health check endpoint."""
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
class NoteViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Notes. User must be authenticated. 
    Only allows access to the notes owned by the authenticated user.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# PUBLIC_INTERFACE
class UserRegistrationView(APIView):
    """
    Registers a new user.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={201: openapi.Response("Created"), 400: "Bad request"},
        operation_summary="Register a new user",
        operation_description="Register a new user with username and password.",
        tags=["authentication"],
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
class LoginView(APIView):
    """
    Authenticates user and returns auth token.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: openapi.Response("Login OK"), 400: "Bad Request", 401: "Unauthorized"},
        operation_summary="Log in",
        operation_description="Authenticate a user and obtain an auth token.",
        tags=["authentication"],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
