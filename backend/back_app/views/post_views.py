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