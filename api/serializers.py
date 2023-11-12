from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from .models import AppUser, Category, Course, Post, Project, Tag


class AppUserSerializer(serializers.ModelSerializer):
    # posts associated with a user: it is not automatically serialized by ModelSerializer
    # posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = AppUser
        fields = ['id', 'email', 'username', 'is_staff']

    def validate_password(self, value):
        return make_password(value)
    

class PostSerializer(serializers.ModelSerializer):
    # serializes only member_id of author: ReadOnly coz it shouldn't be updated using PostUpdateView!
    tags = serializers.SerializerMethodField('get_tags')

    def get_tags(self,obj):
        return [category.title for category in obj.category.all()]
   
    class Meta:
        model = Post
        fields = '__all__'
    

class PostUpdateSerlializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'overview', 'body', 'category', 'slug']
    

class PostFileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['thumbnail']


class ProjectFileUpdateSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['thumbnail']


class CourseFileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['thumbnail']

# class CommentSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     post = serializers.ReadOnlyField(source='post.id')

#     class Meta:
#         model = Comment
#         fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        

class ProjectSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title',
    )

    class Meta:
        model = Project
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title',
    )
    
    class Meta:
        model = Course
        fields = '__all__'
