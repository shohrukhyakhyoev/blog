import json
from django.http import Http404

from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .serializers import AppUserSerializer, CategorySerializer, CourseFileUpdateSerializer, CourseSerializer, PostFileUpdateSerializer, PostSerializer, PostUpdateSerlializer, ProjectFileUpdateSerlializer, ProjectSerializer, TagSerializer
from .models import AppUser, Category, Course, Post, Project, Tag
from .permissions import IsUserItselfOrAdminUser, IsAdminOrReadOnly

from rest_framework import generics, status, permissions, viewsets, filters, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset that handles all request associated with user data
    """
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [IsUserItselfOrAdminUser]


class PostViewSet(viewsets.ModelViewSet):
    """
    Viewset that handles all request associated with post data
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    http_method_names = ['get', 'post', 'delete']


    def get_queryset(self):
        queryset = Post.objects.all().order_by('-timestamp')
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) | Q(body__icontains=q)
                                        | Q(category__title__icontains=q))
        return queryset
    

    def retrieve(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Post, id=pk)
        post_serializer = PostSerializer(instance)
        post = post_serializer.data
        post["thumbnail"] = request.build_absolute_uri(instance.thumbnail.url)
        return Response(post)
    
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    # detail = True makes this func routable
    # @action(detail=True)
    # def comments(self, request, pk):
    #     comments = Comment.objects.filter(post_id=pk)
    #     comments_serializer = CommentSerializer(comments, many=True)
    #     return Response(comments_serializer.data)


class PostUpdateView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get_object(self, pk): 
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
        
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostUpdateSerlializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThumbnailUpdateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def put(self, request, pk, type, format=None):
        if type == 'post':
            obj = Post.objects.filter(id=pk)
            serializer = PostFileUpdateSerializer(obj, data=request.data)
        elif type == 'project':
            obj = Project.objects.filter(id=pk)
            serializer = ProjectFileUpdateSerlializer(obj, data=request.data)
        else:
            obj = Course.objects.filter(id=pk)
            serializer = CourseFileUpdateSerializer(obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset that handles all request associated with category data
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']



class ProjectViewSet(viewsets.ModelViewSet):
    """
    Viewset that handles all request associated with project data
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


    def get_queryset(self):
        queryset = Project.objects.all().order_by('-timestamp')
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) | Q(overview__icontains=q)
                                        | Q(category__title__icontains=q))

        return queryset

    

class TagViewSet(viewsets.ModelViewSet):
    """
    Viewset that handles all request associated with category data
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    """
    Viewset that handles all request associated with academy data
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        queryset = Course.objects.all().order_by('-timestamp')
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) | Q(overview__icontains=q)
                                        | Q(tags__title__icontains=q))
        return queryset
    