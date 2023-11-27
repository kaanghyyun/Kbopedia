from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post

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