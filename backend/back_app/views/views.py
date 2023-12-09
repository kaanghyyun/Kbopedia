# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from django.shortcuts import get_object_or_404
from ..serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# from django.http import HttpResponse, JsonResponse
# from django.contrib.auth import login
# from django.contrib.auth.models import User
# import json
# from django.contrib.auth.decorators import login_required

from ..models import Post, CustomUser
import os
from dotenv import load_dotenv

from django.shortcuts import render, redirect
import requests

load_dotenv()


# Create your views here.
class ListPost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
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


# @csrf_exempt
# def kakao_login(request):
#     # 카카오로부터 받은 인가 코드
#     code = request.GET.get('code', None)
#
#     if code:
#         # 토큰 요청을 위한 파라미터 설정
#         params = {
#             'grant_type': 'authorization_code',
#             'client_id': os.getenv('KAKAO_CLIENT_ID'),
#             'redirect_uri': os.getenv('KAKAO_REDIRECT_URI'),
#             'code': code,
#         }
#
#         # 토큰 요청 보내기
#         response = requests.post('https://kauth.kakao.com/oauth/token', params=params)
#         tokens = response.json()
#
#         # 사용자 정보 요청을 위한 헤더 설정
#         headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
#
#         # 사용자 정보 요청 보내기
#         user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
#         user_info = user_info_response.json()
#
#         # 카카오 계정과 연결된 사용자가 있는지 확인
#         user, created = User.objects.get_or_create(username=user_info['id'])
#
#         # 사용자 로그인 처리
#         login(request, user)
#
#         return HttpResponse(f'Hello, {user.username}!')
#
#     return HttpResponse('Failed to authenticate with Kakao.')


def kakaoLoginLogic(request):
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
    request.session.modified = True

    # 카카오 사용자 정보 가져오기
    user_info_url = 'https://kapi.kakao.com/v2/user/me'
    headers = {'Authorization': f'Bearer {_result["access_token"]}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()
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

    # return redirect('/')
    return redirect('http://localhost:3000')
    # return JsonResponse({'success': True, 'message': 'Login successful', 'user_info': user_info})


def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/unlink'
    _header = {
        'Authorization': f'bearer {_token}'
    }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    if _result.get('id'):
        del request.session['access_token']
        return render(request, 'loginoutSuccess.html')

    else:
        return render(request, 'logoutError.html')