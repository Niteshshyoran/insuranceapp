from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from .serializer import UserSerializer,CompanySerializer,PolicySerializer,ClaimSerializer,PaymentSerializer
from .models import Company,Policy,Claim,Payment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.generics import ListAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView,RetrieveUpdateDestroyAPIView
import jwt,datetime
# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'signup Sucessfull'}, status=status.HTTP_201_CREATED)
        return Response({'message':'invalid credentials'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')


        user = User.objects.filter(username = username).first()
        if user is None:
            return Response({'message':'user not register, please signup'}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({'message':'wrong password, please try again'},status=status.HTTP_400_BAD_REQUEST)
        
        ## creating token
        login(request,user)
        payload = {
            'id':user.id,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.UTC)
        }
        token = jwt.encode(payload, 'cap01',algorithm='HS256')
        response = Response()
        response.data = {'message':'login sucessfull','token':token}
        response.status=status.HTTP_200_OK
        response.set_cookie(
            key='jwt',
            value=token,
            httponly=False,
            samesite=None,
            secure=None,
        )
        return response


class CompanyRegisterView(CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class PolicyRegisterView(CreateAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer

class PolicyUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


class ClaimRegisterView(CreateAPIView):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer


class ClaimUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer


class PaymentRegisterView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
