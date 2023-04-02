from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse  


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.tokens import PasswordResetTokenGenerator 
import six  
class TokenGenerator(PasswordResetTokenGenerator):  
    def _make_hash_value(self, user, timestamp):  
        return (  
            six.text_type(user.pk) + six.text_type(timestamp)
        )  
account_activation_token = TokenGenerator()  

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login_token(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_exists = User.objects.filter(username=serializer.validated_data['username']).exists()
            print(user_exists)
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            
            if user is None:
                data = dict()
                data["message"] = "No user"
                return Response(data, status=404)
            else:
                if user.email_confirmed:
                    refresh = RefreshToken.for_user(user)
                    data = dict()
                    data["refresh"] = str(refresh)
                    data["access"] = str(refresh.access_token)
                    data["username"] = user.username
                    return Response(data, status=200)
                else:
                    data = dict()
                    data["message"] = "Please confirm your email."
                    return Response(data, status=404)
        else:
            data = serializer.errors
            return Response(data, status=409)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.save()
            
            #Send confirm email
            email = user.email
            ######################### mail system ####################################
            htmly = get_template('appuser/Email.html')
            current_site = get_current_site(request)  

            d = { 
                'username': user.username,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
             }
            subject, from_email, to = 'welcome', 'YoutubeAPP@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            data = dict()
            data["message"] = "User registered successfully. Please confirm your email."
            data["email"] = user.email
            
        else:
            data = serializer.errors
            return Response(data, status=409)

        return Response(data, status=201)


def user_confirm_email(request, uidb64, token):
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None

    if user is not None and account_activation_token.check_token(user, token):  
        user.email_confirmed = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  