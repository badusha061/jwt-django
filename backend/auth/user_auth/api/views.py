from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import Userserializers , UserImageserializers
from rest_framework import status
from user_auth.models import UserAccount
from .serializer import Loginserializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate , login
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated


class LoginAPI(APIView):
    def post(self,request):
            data = request.data 
            serializer = Loginserializers(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']
                

                user = authenticate(request=request, email = email , password=password)
                if user is not None:
                    login(request,user)
                if user is None:
                    return Response({
                    'status':400,
                    'message':"Invalid user"
                    })
                else:
                    refresh = RefreshToken.for_user(user)
                    token = {}
                    if user.is_superuser:
                        token['is_admin'] = user.is_superuser
                    else:   
                        token['is_admin'] = False

                    auth_user = Userserializers(user)
                    user_ = {
                        'auth_user':auth_user.data,
                        'token':token,  
                    }
                    return Response({
                        'user':user_,
                        
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
            else:
                return Response({
                    'status':400,
                    'message':"something went wrong"
                })





@api_view(['GET'])
def getRouter(request):
    Routes =[
        'api/token',
        'api/token/refersh',    
    ]
    return Response(Routes)

class UserRegister(APIView):
    def post(self , reqeust):
        serializer= Userserializers(data = reqeust.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)
        
class UserList(APIView):
    def get(self,request):
        users = UserAccount.objects.all()
        serializers = Userserializers(users, many=True)
        return Response(serializers.data)

class UserDetails(APIView):
    def get(self , request,id):
        try:
            user = UserAccount.objects.get(id=id)
            return Response({
                "data":user,
            })
        except UserAccount.DoesNotExist:
            return Response({"errors":"User Not Found"} , status= status.HTTP_400_BAD_REQUEST)
      
    

class UserSoftDelet(APIView):
    def post(self , request,id):
        try:
            user = UserAccount.objects.get(id= id)
            user.is_active = False
            user.save()
            return Response({
                "message":"Successfully Deleted",
            })
        except Exception as e:
            return Response({
                "message":"User Not Found"
            })
        

class UserEdit(APIView):
    def post(self, request, id):
        try:
            user = UserAccount.objects.get(id=id)
            serializer = Userserializers(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)


class UserSearch(APIView):
    def get(self,request, *args, **kwargs):
        try:
            quary = self.kwargs.get('user', '')
            users = UserAccount.objects.filter(first_name__icontains = quary)
            serializer = Userserializers(users,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error":e
            })


class UserAdd(APIView):
    def post(self,request):
        try:
            serializer = Userserializers(data=request.data)
            print('seralizer is the',serializer)
            if serializer.is_valid():
                serializer.save()
                print('saved')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                "error":e
            })


class UserImage(APIView):
    def post(self,request,*args, **kwargs):
        try:
            user = request.user
            serializer= UserImageserializers(data=request.data)
            if serializer.is_valid():
                user = request.user
                user.user_image = serializer.validated_data['user_image']
                user.save()
                return Response(Userserializers(user).data, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            error_message = str(e)
            return Response({
                "error":error_message
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
