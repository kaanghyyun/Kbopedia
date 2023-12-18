# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# from django.http import HttpResponse, JsonResponse
# from django.contrib.auth import login
# from django.contrib.auth.models import User
# import json
# from django.contrib.auth.decorators import login_required

from .models import Post, CustomUser
import os
from dotenv import load_dotenv
 
from django.shortcuts import render, redirect
import requests
from rest_framework.permissions import IsAuthenticated

load_dotenv()


# Create your views here.
class ListPost(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    
class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class IncreaseCount(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.count += 1
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)


def kakaoLoginLogic(request): # 프론트에서 구현 가능
    client_id = os.getenv('KAKAO_CLIENT_ID')  # 입력필요
    redirect_uri = os.getenv('KAKAO_REDIRECT_URI')
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    code = request.GET['code']
    client_id = os.getenv('KAKAO_CLIENT_ID')  # 입력필요
    redirect_uri = os.getenv('KAKAO_REDIRECT_URI')
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}'
    _res = requests.post(_url)
    _result = _res.json()
    request.session['access_token'] = _result['access_token']
    access_token = _result['access_token']
    request.session.modified = True
    print(code)


    # 카카오 사용자 정보 가져오기
    user_info_url = 'https://kapi.kakao.com/v2/user/me'
    headers = {'Authorization': f'Bearer {_result["access_token"]}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()
    kakao_nickname = user_info.get('properties', {}).get('nickname')
    user_id = user_info['id']
    print(user_info)


    user = CustomUser.objects.filter(kakao_user_id=user_info['id']).first()

    if not user:
        # 사용자가 등록되어 있지 않다면 새로운 사용자 생성
        user = CustomUser.objects.create_user(
            username=user_info['id'],
            kakao_user_id=user_info['id'],
            kakao_nickname=user_info.get('properties', {}).get('nickname'),
            kakao_access_token=_result['access_token']

        )

    request.session['access_token'] = _result['access_token']
    request.session.modified = True

    response = JsonResponse({'success': True, 'message': 'Login successful', 'user_info': user_info})
    response.set_cookie('session_token', _result['access_token'])

    front_end_url = 'http://localhost:3000/LoginComponent'
    return redirect(f'{front_end_url}?kakao_nickname={kakao_nickname}&access_token={access_token}&user_id={user_id}')

def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/unlink'
    _header = {
        'Authorization': f'bearer {_token}'
    }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()

    # 세션을 제거
    request.session.clear()

    # return JsonResponse({'success': True, 'message': 'Logged out'})
    return redirect('http://localhost:3000')

def getUserInfo(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return JsonResponse({'error': 'No access token'}, status=401)

    # 카카오 사용자 정보 가져오기
    user_info_url = 'https://kapi.kakao.com/v2/user/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    return JsonResponse({'user_info': user_info})