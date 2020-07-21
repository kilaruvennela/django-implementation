from django.contrib.auth.models import User
from oauth2_provider.models import Application
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import requests
from social_django.models import UserSocialAuth

from .serializers import CreateUserSerializer

CLIENT_ID = "fHD4EVjezPavUHB2c6lgfwduq24iIqtY073mUmvw"
CLIENT_SECRET = "lOhcYPcZg1KxuJOvqBr6rBigP4lVwNVyloXo8ZS2u63RJjPKxvT4kAZKKO56Ah7j7jL4wDtpRC4VlTYHVcm9ox0DN1fGHz2vxsbKKGBoyZKiWGnwQJxqfhj5WEE0RKjt"

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Registers user to the server. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    # Put the data from the request into the serializer 
    serializer = CreateUserSerializer(data=request.data) 
    # Validate the data
    if serializer.is_valid():
        # If it is valid, save the data (creates a user).
        serializer.save() 
        # Then we get a token for the created user.
        # This could be done differentley 
        r = requests.post('http://127.0.0.1:8000/o/token/', 
            data={
                'grant_type': 'password',
                'username': request.data['username'],
                'password': request.data['password'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json())
    return Response(serializer.errors)



@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
    'http://127.0.0.1:8000/o/token/', 
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def convert_token(request):
    '''
    Converts google's access token to the application's access token
    '''

    user = User.objects.filter(is_superuser=True).first().id

    app_client = Application.objects.get(user=user)

    r = requests.post(
        request.build_absolute_uri('/auth/convert-token'),
        data={
            'grant_type': 'convert_token',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'backend':'google-oauth2',
            'token': request.data.get('access_token')
        },
    )
    print('covert', request.user)
    return Response(r.json())

@api_view(['GET'])
@permission_classes([AllowAny])
def check_google_login(request):
    """Checks if a user has signed in with google"""

    print('check', request.user)

    if UserSocialAuth.objects.filter(user_id=request.user.id).exists():
        google_login = {'google_login':True}
        return Response(google_login)
    else:
        google_login = {'google_login': False}
        return Response(google_login)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    '''
    r = requests.post(
    'http://127.0.0.1:8000/o/token/', 
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    r = requests.post(
        'http://127.0.0.1:8000/o/revoke_token/', 
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    # If it goes well return sucess message (would be empty otherwise) 
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    # Return the error if it goes badly
    return Response(r.json(), r.status_code)